#coding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from keepeyes.models import OperationsModel, NotfitOperationsModel, DownloadFilesModel
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from keepeyes.forms import SelectCcForm, CcInputForm, CcModifyForm, ChangePasswordForm
from keepeyes.forms import NotFitSelectCcForm, NotFitCcInputForm, NotFitCcModifyForm
from keepeyes.forms import Approval_Cc_SelectForm, Approval_Cc_Form, DownLoadFile_Form
import datetime
import keepeyes.resources as jzr
from caracate.settings import BASE_DIR
# from django.db.models import Q

MYPAGES = 10

def index(request):
    return render_to_response("index.html",context_instance=RequestContext(request))

@login_required(login_url="/login/")
def cc_select(request, curname="", curppid="", curcounty=""):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    if request.user.unitgroup == 2:
        curhospital = request.user.unitname #医院名称
    else:
        curhospital = ""

    curppname = ["姓名", "性别", "区县", "身份证号", "手术时间", "术眼", "家庭住址", "联系电话", \
        "手术费用", '基金补助', "是否软晶体", "修改"]
    curpp     = []

    if curname == "":
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
    cur_re = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, ppid__icontains=curppid, county__icontains=curcounty)[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, ppid__icontains=curppid, county__icontains=curcounty).count()
    if allPostCounts == 0:
        curPage = 0
        allPage = 0
    # allPostCounts = BlogPost.objects.count()
    allPage = int(allPostCounts / MYPAGES)
    if (allPostCounts % MYPAGES) > 0:
        allPage += 1

    # print allPostCounts, "-----------", allPage, curPage, "+++++++++++++++++++++++++"
    if len(cur_re) != 0:
        for ipp in cur_re:
            if ipp.isapproval == "同意":
                tmpid = ""
            else:
                tmpid = ipp.id
            curpp.append([[ipp.name, ipp.sex, ipp.county, ipp.ppid, ipp.operationtime, ipp.whicheye, \
                ipp.address, ipp.phone, ipp.moneytotal, ipp.moneyfund, ipp.softcrystal], tmpid])
    
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
    
    curpp = OperationsModel.objects.filter(id=curid).exclude(isapproval="同意")
    if len(curpp) == 1:
        curpp = curpp[0]
    else:
        return HttpResponseRedirect('/cc_select/')

    nomodifyinfo = ["姓名：%s"  % curpp.name, "身份证号：%s" % curpp.ppid]

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
def notcc_select(request, curname="", curcounty=""):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curppname = ["姓名", "性别", "区县", "年龄", "住址", "联系电话", "不适合手术原因", "术前检查费", "基金补助",  "ID号", "修改"]
    curpp     = []

    if curname == "":
        if request.method == 'POST':
            curname = request.POST['name'].strip()
            curcounty = request.POST['county']
    form = NotFitSelectCcForm(initial={'name':curname, 'county':curcounty,}) #页面查询窗体

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
    cur_re = NotfitOperationsModel.objects.filter(name__icontains=curname, county__icontains=curcounty)[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = NotfitOperationsModel.objects.filter(name__icontains=curname, county__icontains=curcounty).count()
    if allPostCounts == 0:
        curPage = 0
        allPage = 0
    # allPostCounts = BlogPost.objects.count()
    allPage = int(allPostCounts / MYPAGES)
    if (allPostCounts % MYPAGES) > 0:
        allPage += 1

    # print allPostCounts, "-----------", allPage, curPage, "+++++++++++++++++++++++++"
    if len(cur_re) != 0:
        for ipp in cur_re:
            if ipp.approvaldate:
                tmpid = ""
            else:
                tmpid = ipp.id
            curpp.append([[ipp.name, ipp.sex, ipp.county, ipp.age, ipp.address, ipp.phone, ipp.reason, ipp.moneytotal, ipp.moneyfund, ipp.hospitalID], tmpid])
    
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
        curpp = NotfitOperationsModel.objects.get(id=curid, approvaldate__isnull=True)
    except NotfitOperationsModel.DoesNotExist:
        return HttpResponseRedirect('/notcc_select/')

    nomodifyinfo = ["姓名：%s"  % curpp.name, ]

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
            return notcc_select(request, curpp.name, curpp.county)

    return render_to_response('notcc_applymodify.html', {"form":form, "nomodifyinfo":nomodifyinfo, "jscal_min":jscal_min, "jscal_max":jscal_max}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def cc_approvallist(request, curname="", curcounty="", curhospital=""):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curppname = ["姓名", "性别", "区县", "身份证号", "手术时间", "术眼", "家庭住址", "联系电话", \
        "手术费用", '基金补助', "是否软晶体", "审核"]
    curpp     = []

    if request.method == 'POST':
        curname = request.POST['name'].strip()
        curcounty = request.POST['county']
        curhospital = request.POST['hospital']
    form = Approval_Cc_SelectForm(initial={'name':curname, 'county':curcounty, 'hospital':curhospital,}) #页面查询窗体

    request.session['cc_name'] = curname
    request.session['cc_county'] = curcounty
    request.session['cc_hospital'] = curhospital
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
    cur_re = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, county__icontains=curcounty)[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, county__icontains=curcounty).count()
    if allPostCounts == 0:
        curPage = 0
        allPage = 0
    # allPostCounts = BlogPost.objects.count()
    allPage = int(allPostCounts / MYPAGES)
    if (allPostCounts % MYPAGES) > 0:
        allPage += 1

    # print allPostCounts, "-----------", allPage, curPage, "+++++++++++++++++++++++++"
    if len(cur_re) != 0:
        for ipp in cur_re:
            if ipp.isapproval == "同意":
                tmpflag = 0
            else:
                tmpflag = 1
            curpp.append([[ipp.name, ipp.sex, ipp.county, ipp.ppid, ipp.operationtime, ipp.whicheye, \
                ipp.address, ipp.phone, ipp.moneytotal, ipp.moneyfund, ipp.softcrystal], ipp.id, tmpflag])
    
    return render_to_response("cc_approvallist.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def cc_approvalinput(request, curid=""):
    '''批准视图'''
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    # 如果为空，则跳转到所有申请表中
    if curid == "":
        return HttpResponseRedirect('/cc_approvallist/')

    # 如果已经申批，则跳转
    try:
        curpp = OperationsModel.objects.get(id=curid)
        # curpp = OperationsModel.objects.get(approvaldate__isnull=True,  id=curid)
    except OperationsModel.DoesNotExist:
        return HttpResponseRedirect('/cc_approvallist/')

    nomodifyinfo = ["姓名：%s"  % curpp.name, "手术费用：%s" % curpp.moneytotal, "医院名称：%s" % curpp.hospital]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    btnname = "修改"
    curpp.approvalman = request.user.operatorname
    if curpp.isapproval != "同意":
        btnname = "审核"
        curpp.approvaldate = today
    form = Approval_Cc_Form(instance=curpp)
    if request.method == "POST":
        form = Approval_Cc_Form(request.POST, instance=curpp)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/cc_approvallist/') # Redirect
    return render_to_response('cc_approvalinput.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max, "btnname":btnname}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def cc_onekeyapproval(request):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curname     = request.session['cc_name']
    curcounty   = request.session['cc_county']
    curhospital = request.session['cc_hospital']

    today   = datetime.date.today()
    OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, county__icontains=curcounty \
        ).update(approvalman=request.user.operatorname, moneyfund=1400.00, isapproval="同意", approvaldate=today)

    return cc_approvallist(request, curname, curcounty, curhospital)

@login_required(login_url="/login/")
def notfit_cc_approvallist(request, curname="", curcounty="", curhospital=""):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curppname = ["姓名", "性别", "区县", "年龄", "医院名称", "家庭住址", "联系电话", \
        "手术费用", '基金补助', "不适合手术原因", "医院ID", "审核"]
    curpp     = []

    if request.method == 'POST':
        curname = request.POST['name'].strip()
        curcounty = request.POST['county']
        curhospital = request.POST['hospital']
    form = Approval_Cc_SelectForm(initial={'name':curname, 'county':curcounty, 'hospital':curhospital,}) #页面查询窗体

    request.session['notfitcc_name'] = curname
    request.session['notfitcc_county'] = curcounty
    request.session['notfitcc_hospital'] = curhospital
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
    cur_re = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, county__icontains=curcounty)[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, county__icontains=curcounty).count()
    if allPostCounts == 0:
        curPage = 0
        allPage = 0
    # allPostCounts = BlogPost.objects.count()
    allPage = int(allPostCounts / MYPAGES)
    if (allPostCounts % MYPAGES) > 0:
        allPage += 1

    # print allPostCounts, "-----------", allPage, curPage, "+++++++++++++++++++++++++"
    if len(cur_re) != 0:
        for ipp in cur_re:
            if ipp.isapproval == "同意":
                tmpflag = 0
            else:
                tmpflag = 1
            curpp.append([[ipp.name,ipp.sex,ipp.county,ipp.age,ipp.hospital,ipp.address,\
                ipp.phone,ipp.moneytotal,ipp.moneyfund,ipp.reason,ipp.hospitalID,], ipp.id, tmpflag])
    
    return render_to_response("not_cc_approvallist.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def notfit_cc_approvalinput(request, curid=""):
    '''批准视图'''
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    # 如果为空，则跳转到所有申请表中
    if curid == "":
        return HttpResponseRedirect('/notfit_cc_approvallist/')

    print(1)
    # 如果已经申批，则跳转
    try:
        curpp = NotfitOperationsModel.objects.get(id=curid)
        # curpp = NotfitOperationsModel.objects.get(approvaldate__isnull=True,  id=curid)
    except NotfitOperationsModel.DoesNotExist:
        return HttpResponseRedirect('/notfit_cc_approvallist/')

    nomodifyinfo = ["姓名：%s"  % curpp.name, "检查费用：%s" % curpp.moneytotal, "医院名称:%s" % curpp.hospital]

    today   = datetime.date.today()
    jscal_min = int(today.isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    btnname = "修改"
    curpp.approvalman = request.user.operatorname
    if not curpp.approvaldate:
        btnname = "审核"
        curpp.approvaldate = today
    form = Approval_Cc_Form(instance=curpp)
    if request.method == "POST":
        form = Approval_Cc_Form(request.POST, instance=curpp)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/notfit_cc_approvallist/') # Redirect
    return render_to_response('not_cc_approvalinput.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max, "btnname":btnname}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def notfit_cc_onekeyapproval(request):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curname     = request.session['notfitcc_name']
    curcounty   = request.session['notfitcc_county']
    curhospital = request.session['notfitcc_hospital']

    today   = datetime.date.today()
    cur_re = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, county__icontains=curcounty,)
    if len(cur_re) != 0:
        for ipp in cur_re:
            if ipp.moneytotal >= 350:
                ipp.moneyfund = 350
            else:
                ipp.moneyfund = ipp.moneytotal
            ipp.save()
    
    return notfit_cc_approvallist(request, curname, curcounty, curhospital)

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

@login_required(login_url="/login/")
def downloadfile_list(request, unitname="", datayears=""):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    if request.user.unitgroup == 2:
        unitname = request.user.unitname #单位名称
    else:
        unitname = ""

    curppname = ["单位名称", "年份", "文件"]
    curpp     = []

    if unitname == "":
        if request.method == 'POST':
            unitname    = request.POST['unitname']
            datayears       = request.POST['datayears']
    form = DownLoadFile_Form(initial={'unitname':unitname, 'datayears':datayears}) #页面查询窗体

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
    cur_re = DownloadFilesModel.objects.filter(unitname__icontains=unitname, datayears__icontains=datayears)[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = DownloadFilesModel.objects.filter(unitname__icontains=unitname, datayears__icontains=datayears).count()
    if allPostCounts == 0:
        curPage = 0
        allPage = 0
    # allPostCounts = BlogPost.objects.count()
    allPage = int(allPostCounts / MYPAGES)
    if (allPostCounts % MYPAGES) > 0:
        allPage += 1

    # print allPostCounts, "-----------", allPage, curPage, "+++++++++++++++++++++++++"
    if len(cur_re) != 0:
        for ipp in cur_re:
            curpp.append([[ipp.unitname, ipp.datayears, ipp.filename],])
    
    return render_to_response("download_list.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage},context_instance=RequestContext(request))  

def generate_downfiles(request):
    jzr.writecsv(BASE_DIR)
    return HttpResponseRedirect("/downloadfile_list/")