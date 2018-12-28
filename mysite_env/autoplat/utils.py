#！/usr/bin/env.python
#coding:utf-8

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage


def fen_page(page,obj_list,page_num):
    paginator = Paginator(obj_list,page_num)#每页显示的条数
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        contacts = paginator.page(paginator.num_pages)

    return contacts
