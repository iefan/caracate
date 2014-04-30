#coding=utf8
import keepeyes.resources as jzr
from django import forms
from keepeyes.models import OperationsModel, NotfitOperationsModel
from django.contrib.auth import authenticate
from jzuser.models import MyUser

class ChangePasswordForm(forms.Form):
    '''更改密码视图'''
    # username        = forms.CharField(max_length=100, label="用户名",)
    username        = forms.CharField(max_length=100,widget=forms.HiddenInput())
    oldpassword     = forms.CharField(max_length=100, label="原始密码",widget=forms.PasswordInput())
    newpassword     = forms.CharField(max_length=100, label="新密码",widget=forms.PasswordInput())
    newpassword2    = forms.CharField(max_length=100, label="重复新密码",widget=forms.PasswordInput())
    
    def clean(self):
        return self.cleaned_data

    def clean_oldpassword(self):
        username      = self.cleaned_data['username']
        oldpassword   = self.cleaned_data['oldpassword']
        if oldpassword == "":
            raise forms.ValidationError("请输入原始密码!")
        if not authenticate(username=username, password=oldpassword):
            raise forms.ValidationError("原始密码不正确!")

    def clean_newpassword2(self):
        newpassword = self.cleaned_data['newpassword']
        newpassword2 = self.cleaned_data['newpassword2']
        if newpassword2 != newpassword:
            raise forms.ValidationError("两次输入密码不正确!")

class CcInputForm(forms.ModelForm):
    operationtime   = forms.CharField(error_messages={'required':u'日期不能为空'}, label='手术时间', \
        widget= forms.TextInput())
    
    class Meta:
        model = OperationsModel
        fields = ('name','sex','county','ppid','operationtime','whicheye',\
            'address','phone','moneytotal','hospitalnumber',\
            'softcrystal','hospitalleader','operatorname',)
    def clean(self):
        return self.cleaned_data

    def clean_moneytotal(self):
        moneytotal = self.cleaned_data['moneytotal']
        if moneytotal is None:
            raise forms.ValidationError("请录入手术费用")
        return moneytotal

    def clean_ppid(self):
        ppid   = self.cleaned_data['ppid']
        curpp = OperationsModel.objects.filter(ppid=ppid)
        if len(curpp) != 0:
            raise forms.ValidationError("该身份证号码已录入当前系统！")
        else:
            pass
        return ppid    

class CcModifyForm(forms.ModelForm):
    operationtime   = forms.CharField(error_messages={'required':u'日期不能为空'}, label='手术时间', \
        widget= forms.TextInput())
    
    class Meta:
        model = OperationsModel
        fields = ('sex','county','operationtime','whicheye',\
            'address','phone','moneytotal','hospitalnumber',\
            'softcrystal','hospitalleader','operatorname',)
        # exclude=('name','ppid',)

    def clean(self):
        return self.cleaned_data

    def clean_ppid(self):
        ppid   = self.cleaned_data['ppid']        
        return ppid

    def clean_phone(self):
        phone  = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone)<11 or len(phone) > 12:
            raise forms.ValidationError("请输入11或12位电话号码")
        return phone


class NotFitCcInputForm(forms.ModelForm):

    class Meta:
        model = NotfitOperationsModel
        fields = ('name','sex','county','age','hospital','address','phone',\
            'moneytotal', 'hospitalleader','reason','hospitalID','operatorname',)

    def clean(self):
        return self.cleaned_data

    def clean_moneytotal(self):
        moneytotal = self.cleaned_data['moneytotal']
        if moneytotal is None:
            raise forms.ValidationError("请录入手术费用")
        return moneytotal

    def clean_phone(self):
        phone  = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone)<11 or len(phone) > 12:
            raise forms.ValidationError("请输入11或12位电话号码")
        return phone

class NotFitCcModifyForm(forms.ModelForm):
    class Meta:
        model = NotfitOperationsModel
        fields = ('county','age','hospital','address','phone',\
            'moneytotal','moneyfund','hospitalleader','reason','hospitalID','operatorname',)
        # exclude=('name','ppid',)

    def clean(self):
        return self.cleaned_data

    def clean_phone(self):
        phone  = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone)<11 or len(phone) > 12:
            raise forms.ValidationError("请输入11或12位电话号码")
        return phone


class NotFitSelectCcForm(forms.ModelForm):
    '''不适合白内障手术查询条件表单'''
    lstcounty = list(jzr.COUNTY_CHOICES)
    lstcounty.insert(0, ("", "--"))
    county = forms.ChoiceField(choices = tuple(lstcounty), label="区县名称",)
    class Meta:
        model = NotfitOperationsModel
        fields = ('name', 'county',)

    def clean(self):
        return self.cleaned_data

class SelectCcForm(forms.ModelForm):
    '''白内障手术查询条件表单'''
    lstcounty = list(jzr.COUNTY_CHOICES)
    lstcounty.insert(0, ("", "--"))
    county = forms.ChoiceField(choices = tuple(lstcounty), label="区县名称",)
    class Meta:
        model = OperationsModel
        fields = ('name', 'ppid', 'county',)

    def clean(self):
        return self.cleaned_data

class Approval_Cc_SelectForm(forms.ModelForm):
    '''审核白内障手术查询条件表单'''
    lsthospital = list(jzr.HOSPITAL_CHOICES)
    lsthospital.insert(0, ("", "--"))
    hospital = forms.ChoiceField(choices = tuple(lsthospital), label="医院名称",)
    lstcounty = list(jzr.COUNTY_CHOICES)
    lstcounty.insert(0, ("", "--"))
    county = forms.ChoiceField(choices = tuple(lstcounty), label="区县名称",)
    class Meta:
        model = OperationsModel
        fields = ('name', 'county', 'hospital',)

    def clean(self):
        return self.cleaned_data

class Approval_Cc_Form(forms.ModelForm):
    """申批表"""
    # caracate = forms.ModelChoiceField(queryset=OperationsModel.objects.all(), widget=forms.HiddenInput())
    approvaldate   = forms.CharField(error_messages={'required':u'日期不能为空'}, label='办证时间', \
        widget= forms.TextInput())
    
    class Meta:
        model = OperationsModel
        fields = ('moneyfund', 'isapproval', 'approvaldate', 'approvalman',)
       
    def clean(self):
        return self.cleaned_data

