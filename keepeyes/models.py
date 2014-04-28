#coding=utf8
from django.db import models
import keepeyes.resources as jzr
# from datetime import date

class OperationsModel(models.Model):
    name            = models.CharField(max_length=30, verbose_name="姓名")
    sex             = models.CharField(choices=jzr.SEX_CHOICES, max_length=2, verbose_name="性别", default="男")
    county          = models.CharField(choices=jzr.COUNTY_CHOICES, max_length=30, verbose_name="区县", default="金平区")
    ppid            = models.CharField(unique=True, max_length=30, verbose_name="身份证号")
    operationtime   = models.DateField(verbose_name="手术时间", blank=True, null=True, )
    hospital        = models.CharField(choices=jzr.HOSPITAL_CHOICES, max_length=30, verbose_name="医院名称", default="国际眼科中心")
    whicheye        = models.CharField(choices=jzr.EYE_CHOICES, max_length=10, verbose_name="术眼", default="左眼")
    address         = models.CharField(max_length=100, verbose_name="住址", blank=True, null=True, )
    phone           = models.CharField(max_length=20, verbose_name="固定电话",blank=True, null=True,)
    phone2          = models.CharField(max_length=20, verbose_name="手机",blank=True, null=True,)
    moneytotal      = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="手术费用", blank=True, null=True,)
    moneyfund       = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="基金补助", blank=True, null=True,)
    hospitalnumber  = models.CharField(max_length=30, verbose_name="住院号",blank=True, null=True,)
    softcrystal     = models.CharField(max_length=30, verbose_name="是否软晶体", choices=jzr.YESNO_CHOICE, default="是")
    operatorname    = models.CharField(max_length=30, verbose_name='录入人员', blank=True, null=True,)
    hospitalleader  = models.CharField(max_length=30, verbose_name="医院负责人", blank=True, null=True, )
    isapproval      = models.CharField(max_length=30, verbose_name="残联审核", choices=jzr.ISAPPROVAL_CHOICES, default="待审",)
    approvaldate    = models.DateField(verbose_name="审核时间", blank=True, null=True)
    approvalman     = models.CharField(max_length=30, verbose_name="审核人员", blank=True, null=True,)

    class Meta:
        ordering = ['county',]
        verbose_name = "手术人员信息"  
        verbose_name_plural = "手术人员信息"  
        # app_label = u"信息管理"

    def __unicode__(self):
        return "%s %s %s %s %s %s %s %s %s" % (self.name, self.county, self.operationtime, \
            self.hospital, self.whicheye, self.phone, self.moneytotal, self.operatorname, self.approvalman,)

class NotfitOperationsModel(models.Model):
    name            = models.CharField(max_length=30, verbose_name="姓名")
    sex             = models.CharField(choices=jzr.SEX_CHOICES, max_length=2, verbose_name="性别", default="男")
    county          = models.CharField(choices=jzr.COUNTY_CHOICES, max_length=30, verbose_name="区县", default="金平区")
    age             = models.CharField(max_length=3, blank=True, null=True, verbose_name="年龄")
    hospital        = models.CharField(choices=jzr.HOSPITAL_CHOICES, max_length=30, verbose_name="医院名称", default="国际眼科中心")
    address         = models.CharField(max_length=100, verbose_name="住址", blank=True, null=True, )
    phone           = models.CharField(max_length=20, verbose_name="固定电话",blank=True, null=True,)
    moneytotal      = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="手术费用", blank=True, null=True,)
    moneyfund       = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="基金补助", blank=True, null=True,)
    operatorname    = models.CharField(max_length=30, verbose_name='录入人员', blank=True, null=True,)
    hospitalleader  = models.CharField(max_length=30, verbose_name="医院负责人", blank=True, null=True, )
    reason          = models.CharField(choices=jzr.SEX_CHOICES, max_length=40, verbose_name="不适合手术原因", default="男")
    hospitalID      = models.CharField(max_length=30, verbose_name="挂号ID", blank=True, null=True, )
    isapproval      = models.CharField(max_length=30, verbose_name="残联审核", choices=jzr.ISAPPROVAL_CHOICES, default="待审",)
    approvaldate    = models.DateField(verbose_name="审核时间", blank=True, null=True)
    approvalman     = models.CharField(max_length=30, verbose_name="审核人员", blank=True, null=True,)

    class Meta:
        ordering = ['county',]
        verbose_name = "不适合手术人员信息"  
        verbose_name_plural = "不适合手术人员信息"  
        # app_label = u"信息管理"

    def __unicode__(self):
        return "%s %s %s %s %s %s %s %s" % (self.name, self.county, self.reason, \
            self.hospital, self.phone, self.moneytotal, self.operatorname, self.approvalman,)
