
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import HttpResponse, render
from cmdb.forms import AssetForm
from cmdb.models import ASSET_STATUS, ASSET_TYPE, Host, HostGroup, Idc, Cabinet
from cmdb.api import get_object, pages

def asset(request):
    temp_name = "cmdb/cmdb-header.html"
    asset_find = []
    idc_info = Idc.objects.all()
    group_info = HostGroup.objects.all()
    asset_types = ASSET_TYPE
    asset_status = ASSET_STATUS
    idc_name = request.GET.get('idc', '')
    page_len = request.GET.get('page_len', '')
    group_name = request.GET.get('group', '')
    asset_type = request.GET.get('asset_type', '')
    status = request.GET.get('status', '')
    keyword = request.GET.get('keyword', '')
    export = request.GET.get("export", '')
    group_id = request.GET.get("group_id", '')
    cabinet_id = request.GET.get("cabinet_id", '')
    idc_id = request.GET.get("idc_id", '')
    asset_id_all = request.GET.getlist("id", '')

    if group_id:
        group = get_object(HostGroup, id=group_id)
        if group:
            asset_find = Host.objects.filter(group=group)

    if cabinet_id:
        cabinet = get_object(Cabinet, id=cabinet_id)
        if cabinet:
            asset_find = Host.objects.filter(cabinet=cabinet)

    elif idc_id:
        idc = get_object(Idc, id=idc_id)
        if idc:
            asset_find = Host.objects.filter(idc=idc)
    else:
        asset_find = Host.objects.all()
    if idc_name:
        asset_find = asset_find.filter(idc__name__contains=idc_name)
    if group_name:
        get_group = HostGroup.objects.get(name=group_name)
        asset_find = get_group.serverList.all()
    if asset_type:
        asset_find = asset_find.filter(asset_type__contains=asset_type)
    if status:
        asset_find = asset_find.filter(status__contains=status)
    if keyword:
        asset_find = asset_find.filter(
            Q(hostname__contains=keyword) |
            Q(ip__contains=keyword) |
            Q(other_ip__contains=keyword) |
            Q(os__contains=keyword) |
            Q(vendor__contains=keyword) |
            Q(cpu_model__contains=keyword) |
            Q(cpu_num__contains=keyword) |
            Q(memory__contains=keyword) |
            Q(disk__contains=keyword) |
            Q(sn__contains=keyword) |
            Q(position__contains=keyword) |
            Q(memo__contains=keyword))
    assets_list, p, assets, page_range, current_page, show_first, show_end, end_page = pages(asset_find, request)
    return render(request, 'cmdb/index.html', locals())