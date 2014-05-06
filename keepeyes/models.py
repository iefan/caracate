#coding=utf8
from django.db import models
import keepeyes.resources as jzr
from django.utils.http import urlquote
import datetime
# from datetime import date

class OperationsModel(models.Model):
    name            = models.CharField(max_length=30, verbose_name="姓名")
    sex             = models.CharField(choices=jzr.SEX_CHOICES, max_length=2, verbose_name="性别", default="男")
    county          = models.CharField(choices=jzr.COUNTY_CHOICES, max_length=30, verbose_name="区县", default="金平区")
    ppid            = models.CharField(max_length=30, verbose_name="身份证号")
    operationtime   = models.DateField(verbose_name="手术时间", )
    hospital        = models.CharField(choices=jzr.HOSPITAL_CHOICES, max_length=30, verbose_name="医院名称", default="国际眼科中心")
    whicheye        = models.CharField(choices=jzr.EYE_CHOICES, max_length=10, verbose_name="术眼", default="左眼")
    address         = models.CharField(max_length=100, verbose_name="住址", blank=True, null=True, )
    phone           = models.CharField(max_length=20, verbose_name="联系电话",blank=True, null=True,)
    moneytotal      = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="手术费用", blank=True, null=True,)
    moneyfund       = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="基金补助", blank=True, null=True,)
    hospitalnumber  = models.CharField(max_length=30, verbose_name="住院号",blank=True, null=True,)
    softcrystal     = models.CharField(max_length=30, verbose_name="是否软晶体", choices=jzr.ISSOFT_CHOICE, default="是")
    operatorname    = models.CharField(max_length=30, verbose_name='录入人员', blank=True, null=True,)
    isapproval      = models.CharField(max_length=30, verbose_name="残联审核", choices=jzr.ISAPPROVAL_CHOICES, blank=True, null=True)
    approvaldate    = models.DateField(verbose_name="审核时间", blank=True, null=True)
    approvalman     = models.CharField(max_length=30, verbose_name="审核人员", blank=True, null=True,)

    class Meta:
        ordering = ['county',]
        verbose_name = "手术人员信息"  
        verbose_name_plural = "手术人员信息"  
        # app_label = u"信息管理"

    def __str__(self):
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
    reason          = models.CharField(max_length=40, verbose_name="不适合手术原因", )
    hospitalID      = models.CharField(max_length=30, verbose_name="挂号ID", blank=True, null=True, )
    checkdate       = models.DateField(verbose_name="检查日期")
    moneytotal      = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="手术费用", blank=True, null=True,)
    moneyfund       = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="基金补助", blank=True, null=True,)
    operatorname    = models.CharField(max_length=30, verbose_name='录入人员', blank=True, null=True,)
    isapproval      = models.CharField(max_length=30, verbose_name="残联审核", choices=jzr.ISAPPROVAL_CHOICES,  blank=True, null=True)
    approvaldate    = models.DateField(verbose_name="审核时间", blank=True, null=True)
    approvalman     = models.CharField(max_length=30, verbose_name="审核人员", blank=True, null=True,)

    class Meta:
        ordering = ['county',]
        verbose_name = "不适合手术人员信息"  
        verbose_name_plural = "不适合手术人员信息"  
        # app_label = u"信息管理"

    def __str__(self):
        return "%s %s %s %s %s %s %s %s" % (self.name, self.county, self.reason, \
            self.hospital, self.phone, self.moneytotal, self.operatorname, self.approvalman,)

class DownloadFilesModel(models.Model):
    unitname        = models.CharField(choices=jzr.UNIT_CHOICES, max_length=30, verbose_name="单位名称")
    datayears       = models.CharField(max_length=100, verbose_name="年份")
    filename        = models.CharField(max_length=100, verbose_name="文件位置")
    updatetime      = models.DateField(verbose_name="更新时间", blank=True, null=True)
   
    class Meta:
        ordering = ['datayears',]
        verbose_name = "文件下载信息"  
        verbose_name_plural = "文件下载信息"  
        # app_label = u"信息管理"

    def __str__(self):
        return "%s %s %s " % (self.unitname, self.datayears, self.filename, )


class AddressBookModel(models.Model):
    name            = models.CharField(max_length=50, verbose_name="姓名")
    unitname        = models.CharField(choices=jzr.UNITNAMES_CHOICES, max_length=30, verbose_name="单位")
    phone           = models.CharField(max_length=100, verbose_name="电话")
    email           = models.CharField(max_length=100, verbose_name="邮箱", blank=True, null=True)
   
    class Meta:
        ordering = ['unitname',]
        verbose_name = "通迅录"  
        verbose_name_plural = "通迅录"  
        # app_label = u"信息管理"

    def __str__(self):
        return "%s %s %s %s " % (self.name, self.unitname, self.phone, self.email)

class GMXModel(models.Model):
    #当月筛查例数 当月手术例数  光明行下乡次数
    thisyear = str(datetime.date.today()).split("-")[0]
    lstmonth = []
    for imonth in list(range(1,13)):
        lstmonth.append((thisyear+"-"+str(imonth), thisyear+"-"+str(imonth)))
    # lstmonth = [(datetime.date(int(thisyear), imonth, 1), thisyear+"-"+str(imonth)) for imonth in list(range(1,13))]

    whichmonth      = models.CharField(choices=lstmonth, max_length=30, verbose_name="月份")
    unitname        = models.CharField(choices=jzr.HOSPITAL_CHOICES, max_length=30, verbose_name="单位")
    checknums       = models.IntegerField(verbose_name="当月筛查例数", blank=True, null=True)
    operatornums    = models.IntegerField(verbose_name="当月手术例数", blank=True, null=True)
    gmxnums         = models.IntegerField(verbose_name="光明行下乡次数", blank=True, null=True)

    class Meta:
        ordering = ['whichmonth',]
        verbose_name = "光明行项目进展表"  
        verbose_name_plural = "光明行项目进展表" 

    def __str__(self):
        return "%s %s %s %s %s " % (self.whichmonth, self.unitname, self.checknums, self.operatornums, self.gmxnums)
