#coding=utf8
import keepeyes.resources as jzr
from django import forms
from keepeyes.models import OperationsModel
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
        fields = ('name','sex','county','ppid','operationtime','hospital','whicheye',\
            'address','phone','phone2','moneytotal','hospitalnumber',\
            'softcrystal','operatorname','hospitalleader',)
    def clean(self):
        return self.cleaned_data

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
        fields = ('sex','county','operationtime','hospital','whicheye',\
            'address','phone','phone2','moneytotal','hospitalnumber',\
            'softcrystal','operatorname','hospitalleader',)
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