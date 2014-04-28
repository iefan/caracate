#coding=utf8
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from keepeyes.models import OperationsModel, NotfitOperationsModel
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from keepeyes.forms import SelectCcForm, CcInputForm, CcModifyForm, ChangePasswordForm, NotFitCcInputForm, NotFitCcModifyForm
import datetime

MYPAGES = 10

def index(request):
    return render_to_response("index.html",context_instance=RequestContext(request))

@login_required(login_url="/login/")
def cc_select(request, curname="", curppid="", curcounty=""):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curppname = [u"姓名", u"区县", u"身份证号", u"手术时间", u"手术费用", u"联系电话", u"是否软晶体", u"修改"]
    curpp     = []

    if request.method == 'POST':
        curname = request.POST['name'].strip()
        curppid = request.POST['ppid'].strip()
        curcounty = request.POST['county']
    form = SelectCcForm(initial={'name':curname, 'ppid':curppid, 'county':curcounty,}) #页面查询窗体

    #=====================new page=================
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPostCounts = int(request.GET.get('allPostCounts',''))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPostCounts = ""
        pageType = ''

    if curPage < 1:
        curPage = 1
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    startPos = (curPage-1) * MYPAGES
    endPos = startPos + MYPAGES
    cur_re = OperationsModel.objects.filter(name__icontains=curname, ppid__icontains=curppid, county__icontains=curcounty)[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = OperationsModel.objects.filter(name__icontains=curname, ppid__icontains=curppid, county__icontains=curcounty).count()
    if allPostCounts == 0:
        curPage = 0
        allPage = 0
    # allPostCounts = BlogPost.objects.count()
    allPage = allPostCounts / MYPAGES
    if (allPostCounts % MYPAGES) > 0:
        allPage += 1

    # print allPostCounts, "-----------", allPage, curPage, "+++++++++++++++++++++++++"
    if len(cur_re) != 0:
        for ipp in cur_re:
            curphone = ipp.phone
            if ipp.phone == "":
                curphone = ipp.phone2
            curpp.append([[ipp.name,  ipp.county, ipp.ppid, ipp.operationtime, ipp.moneytotal, curphone, ipp.softcrystal], ipp.id])
    
    return render_to_response("cc_applylist.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def cc_input(request):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    # request.session['gameclass'] = ""
    today   = datetime.date.today()

    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    form = CcInputForm(initial={'operatorname':request.user.operatorname, 'hospital':request.user.unitname})
    # print form
    # gameclass = request.session['gameclass']
    if request.method == "POST":
        form = CcInputForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cc_select/') # Redirect
    return render_to_response('cc_applyinput.html', {"form":form,"jscal_min":jscal_min, "jscal_max":jscal_max}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def cc_modify(request, curid="0"):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    if curid == "0":
        return HttpResponseRedirect('/cc_select/')
    
    try:
        curpp = OperationsModel.objects.get(id=curid)
    except OperationsModel.DoesNotExist:
        return HttpResponseRedirect('/cc_select/')

    nomodifyinfo = [u"姓名：%s"  % curpp.name, u"身份证号：%s" % curpp.ppid]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    curpp.operatorname = request.user.operatorname
    curpp.hospital = request.user.unitname
    form = CcModifyForm(instance=curpp)
    if request.method == "POST":
        form = CcModifyForm(request.POST, instance=curpp) # this can modify the current form
        if form.is_valid():
            form.save()
            return cc_select(request, curpp.name, curpp.ppid)

    return render_to_response('cc_applymodify.html', {"form":form, "nomodifyinfo":nomodifyinfo, "jscal_min":jscal_min, "jscal_max":jscal_max}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def notcc_select(request, curname="", curppid="", curcounty=""):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curppname = ["姓名", "性别", "区县", "年龄", "住址", "联系电话", "不适合手术原因", "修改"]
    crpp     = []

    if request.method == 'POST':
        curname = request.POST['name'].strip()
        curppid = request.POST['ppid'].strip()
        curcounty = request.POST['county']
    form = SelectCcForm(initial={'name':curname, 'ppid':curppid, 'county':curcounty,}) #页面查询窗体

    #=====================new page=================
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPostCounts = int(request.GET.get('allPostCounts',''))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPostCounts = ""
        pageType = ''

    if curPage < 1:
        curPage = 1
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    startPos = (curPage-1) * MYPAGES
    endPos = startPos + MYPAGES
    cur_re = NotfitOperationsModel.objects.filter(name__icontains=curname, ppid__icontains=curppid, county__icontains=curcounty)[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = NotfitOperationsModel.objects.filter(name__icontains=curname, ppid__icontains=curppid, county__icontains=curcounty).count()
    if allPostCounts == 0:
        curPage = 0
        allPage = 0
    # allPostCounts = BlogPost.objects.count()
    allPage = allPostCounts / MYPAGES
    if (allPostCounts % MYPAGES) > 0:
        allPage += 1

    # print allPostCounts, "-----------", allPage, curPage, "+++++++++++++++++++++++++"
    if len(cur_re) != 0:
        for ipp in cur_re:
            curpp.append([[ipp.name, ipp.sex, ipp.county, ipp.age, ipp.address, ipp.phone, ipp.reason], ipp.id])
    
    return render_to_response("notcc_applylist.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def notcc_input(request):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    # request.session['gameclass'] = ""
    today   = datetime.date.today()

    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    form = NotFitCcInputForm(initial={'operatorname':request.user.operatorname, 'hospital':request.user.unitname})
    # print form
    # gameclass = request.session['gameclass']
    if request.method == "POST":
        form = NotFitCcInputForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/notcc_select/') # Redirect
    return render_to_response('notcc_applyinput.html', {"form":form,"jscal_min":jscal_min, "jscal_max":jscal_max}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def notcc_modify(request, curid="0"):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    if curid == "0":
        return HttpResponseRedirect('/notcc_select/')
    
    try:
        curpp = NotfitOperationsModel.objects.get(id=curid)
    except NotfitOperationsModel.DoesNotExist:
        return HttpResponseRedirect('/notcc_select/')

    nomodifyinfo = [u"姓名：%s"  % curpp.name, u"身份证号：%s" % curpp.ppid]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    curpp.operatorname = request.user.operatorname
    curpp.hospital = request.user.unitname
    form = NotFitCcModifyForm(instance=curpp)
    if request.method == "POST":
        form = NotFitCcModifyForm(request.POST, instance=curpp) # this can modify the current form
        if form.is_valid():
            form.save()
            return notcc_select(request, curpp.name, curpp.ppid)

    return render_to_response('notcc_applymodify.html', {"form":form, "nomodifyinfo":nomodifyinfo, "jscal_min":jscal_min, "jscal_max":jscal_max}, context_instance=RequestContext(request))


@login_required(login_url="/login/")
def changepassword(request):
    user = request.user
    form = ChangePasswordForm(initial={'username':user.unitsn})
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            newpassword = request.POST['newpassword']
            user.set_password(newpassword)
            user.save()
            return HttpResponseRedirect("/login/")
    return render_to_response('changepassword.html', {'form':form,}, context_instance=RequestContext(request))