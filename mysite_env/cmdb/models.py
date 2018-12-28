from __future__ import unicode_literals
from django.db import models

ASSET_OWERNER = (
    (0, "ayla"),
    (1, "sunsea"))

ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
    )

ASSET_TYPE = (
    (str(1), u"物理机"),
    (str(2), u"虚拟机"),
    (str(3), u"容器")
    )

class Host(models.Model):
    hostname = models.CharField(max_length=50, verbose_name=u"主机名", unique=True)
    ip = models.GenericIPAddressField(u"IP", max_length=15)
    asset_no = models.CharField(u"资产编号", max_length=50, blank=True)
    asset_type = models.CharField(u"设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True)
    relation = models.IntegerField(u"设备所属",choices=ASSET_OWERNER, default=1)
    status = models.CharField(u"设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    os = models.CharField(u"操作系统", max_length=100, blank=True)
    cpu_num = models.CharField(u"CPU数量", max_length=100, blank=True)
    memory = models.CharField(u"内存大小", max_length=30, blank=True)
    memo = models.TextField(u"备注信息", max_length=200, blank=True)

    def __unicode__(self):
        return self.hostname


