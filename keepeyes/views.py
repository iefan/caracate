#coding=utf8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from keepeyes.models import OperationsModel, NotfitOperationsModel, DownloadFilesModel, AddressBookModel, GMXModel
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from keepeyes.forms import SelectCcForm, CcInputForm, CcModifyForm, ChangePasswordForm
from keepeyes.forms import NotFitSelectCcForm, NotFitCcInputForm, NotFitCcModifyForm, GMX_Form, GMX_input_Form
from keepeyes.forms import Approval_Cc_SelectForm, Approval_Cc_Form, DownLoadFile_Form, InitUserPasswordForm
import datetime, os, base64
import keepeyes.resources as jzr
from jzuser.models import MyUser
from caracate.settings import BASE_DIR
# from django.core.servers.basehttp import FileWrapper
from django.utils.http import urlquote
# from django.db.models import Q

MYPAGES = 10

def index(request):
    return render_to_response("index.html",context_instance=RequestContext(request))

@login_required(login_url="/login/")
def cc_select(request, curid=""):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    if int(request.user.unitgroup) == 2:
        curhospital = request.user.unitname #医院名称
    else:
        curhospital = "" #市残联

    curppname = ["姓名", "性别", "区县", "身份证号", "手术时间", "术眼", "联系电话", \
        "手术费用", '基金补助', "是否软晶体", "家庭住址", "修改"]
    curpp     = []

    (curname, curyears, curisapproval) = ("", "", "")
    if curid == "":
        if request.method == 'POST':
            curname         = request.POST['name'].strip()
            curisapproval   = request.POST['isapproval']
            curyears        = request.POST['whichyears']
    else:
        modifypp        = OperationsModel.objects.get(id=curid)
        curname         = modifypp.name
        curisapproval   = modifypp.isapproval
        curyears        = modifypp.operationtime.year

    #=====================new page=================
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPostCounts = int(request.GET.get('allPostCounts',''))
        pageType = str(request.GET.get('pageType', ''))
        get_select_str = str(request.GET.get("get_select_str", "||"))
    except ValueError:
        curPage = 1
        allPostCounts = ""
        pageType = ''
        get_select_str = "||"

    if get_select_str != "||":
        (curname, curyears, curisapproval) = get_select_str.split("|")
    form = SelectCcForm(initial={'name':curname, 'whichyears':curyears, 'isapproval':curisapproval}) #页面查询窗体
    get_select_str = "|".join([curname, str(curyears), curisapproval])
    
    if curPage < 1:
        curPage = 1
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    startPos = (curPage-1) * MYPAGES
    endPos = startPos + MYPAGES
    if curyears == "":
        cur_re = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, isapproval__icontains=curisapproval).order_by('-operationtime')[startPos:endPos]
    else:
        cur_re = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, operationtime__year=int(curyears), isapproval__icontains=curisapproval).order_by('-operationtime')[startPos:endPos]

    if allPostCounts == "": #标记1
        if curyears == "":
            allPostCounts = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, isapproval__icontains=curisapproval).count()
        else:
            allPostCounts = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, operationtime__year=int(curyears), isapproval__icontains=curisapproval).count()
    if allPostCounts == 0:
        curPage = 0
        allPage = 0
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
                 ipp.phone, ipp.moneytotal, ipp.moneyfund, ipp.softcrystal, ipp.address,], tmpid])
    
    return render_to_response("cc_applylist.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage, "get_select_str":get_select_str,},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def cc_input(request):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    thisday = datetime.date.today()
    jscal_min = (datetime.date(thisday.year, 1, 1).isoformat().replace('-', ''))
    jscal_max = int(thisday.isoformat().replace('-', ''))

    form = CcInputForm(initial={'operatorname':request.user.operatorname, 'hospital':request.user.unitname, 'isapproval':"待审"})
    if request.method == "POST":
        form = CcInputForm(request.POST)
        if form.is_valid():
            savepp = form.save()
            return cc_select(request, savepp.id)
    return render_to_response('cc_applyinput.html', {"form":form,"jscal_min":jscal_min, "jscal_max":jscal_max}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def cc_modify(request, curid=""):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    if curid == "":
        return HttpResponseRedirect('/cc_select/')
    
    curpp = OperationsModel.objects.filter(id=curid).exclude(isapproval="同意")
    if len(curpp) == 1:
        curpp = curpp[0]
    else:
        return HttpResponseRedirect('/cc_select/')

    nomodifyinfo = ["姓名：%s"  % curpp.name, "身份证号：%s" % curpp.ppid]

    # thisday   = datetime.date(curpp.operationtime.year, curpp.operationtime.month, 1)
    thisday   = datetime.date.today()
    jscal_min = (datetime.date(thisday.year, 1, 1).isoformat().replace('-', ''))
    # jscal_min = int((thisday - datetime.timedelta(60)).isoformat().replace('-', ''))
    jscal_max = int(thisday.isoformat().replace('-', ''))

    curpp.operatorname = request.user.operatorname
    curpp.hospital = request.user.unitname
    form = CcModifyForm(instance=curpp)
    if request.method == "POST":
        form = CcModifyForm(request.POST, instance=curpp) # this can modify the current form
        if form.is_valid():
            form.save()
            return cc_select(request, curpp.id)

    return render_to_response('cc_applymodify.html', {"form":form, "nomodifyinfo":nomodifyinfo, "jscal_min":jscal_min, "jscal_max":jscal_max}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def notcc_select(request, curid=""):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    if int(request.user.unitgroup) == 2:
        curhospital = request.user.unitname #医院名称
    else:
        curhospital = "" #市残联

    curppname = ["姓名", "性别", "区县", "年龄", "联系电话", "不适合手术原因", "术前检查费", "基金补助",  "ID号", "月份", "住址", "修改"]
    curpp     = []

    (curname, curyears, curisapproval) = ("", "", "")
    if curid == "":
        if request.method == 'POST':
            curname         = request.POST['name'].strip()
            curisapproval   = request.POST['isapproval']
            curyears        = request.POST['whichyears']
    else:
        modifypp        = NotfitOperationsModel.objects.get(id=curid)
        curname         = modifypp.name
        curisapproval   = modifypp.isapproval
        curyears        = modifypp.checkdate.year

    #=====================new page=================
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPostCounts = int(request.GET.get('allPostCounts',''))
        pageType = str(request.GET.get('pageType', ''))
        get_select_str = str(request.GET.get("get_select_str", "||"))
    except ValueError:
        curPage = 1
        allPostCounts = ""
        pageType = ''
        get_select_str = "||"


    if get_select_str != "||":
        (curname, curyears, curisapproval) = get_select_str.split("|")
    form = NotFitSelectCcForm(initial={'name':curname, 'whichyears':curyears, 'isapproval':curisapproval}) #页面查询窗体
    get_select_str = "|".join([curname, str(curyears), curisapproval])

    if curPage < 1:
        curPage = 1
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    startPos = (curPage-1) * MYPAGES
    endPos = startPos + MYPAGES
    if curyears == "":
        cur_re = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, isapproval__icontains=curisapproval).order_by('-checkdate')[startPos:endPos]
    else:
        cur_re = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, checkdate__year=int(curyears), isapproval__icontains=curisapproval).order_by('-checkdate')[startPos:endPos]

    # cur_re = NotfitOperationsModel.objects.filter(name__icontains=curname, county__icontains=curcounty)[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        if curyears == "":
            allPostCounts = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, isapproval__icontains=curisapproval).count()
        else:
            allPostCounts = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, checkdate__year=int(curyears), isapproval__icontains=curisapproval).count()

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
            curpp.append([[ipp.name, ipp.sex, ipp.county, ipp.age, ipp.phone, ipp.reason, ipp.moneytotal, ipp.moneyfund, ipp.hospitalID, ipp.checkdate, ipp.address,], tmpid])
    
    return render_to_response("notcc_applylist.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage, 'get_select_str':get_select_str},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def notcc_input(request):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    thisday = datetime.date.today()
    jscal_min = (datetime.date(thisday.year, 1, 1).isoformat().replace('-', ''))
    # jscal_min = int((thisday - datetime.timedelta(60)).isoformat().replace('-', ''))
    jscal_max = int(thisday.isoformat().replace('-', ''))
    
    form = NotFitCcInputForm(initial={'operatorname':request.user.operatorname, 'hospital':request.user.unitname, 'isapproval':"待审"})
    # print form
    # gameclass = request.session['gameclass']
    if request.method == "POST":
        form = NotFitCcInputForm(request.POST)
        if form.is_valid():
            savepp = form.save()
            return notcc_select(request, savepp.id)
    return render_to_response('notcc_applyinput.html', {"form":form,"jscal_min":jscal_min, "jscal_max":jscal_max}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def notcc_modify(request, curid=""):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    if curid == "":
        return HttpResponseRedirect('/notcc_select/')
    
    curpp = NotfitOperationsModel.objects.filter(id=curid).exclude(isapproval="同意")
    if len(curpp) == 1:
        curpp = curpp[0]
    else:
        return HttpResponseRedirect('/cc_select/')

    nomodifyinfo = ["姓名：%s"  % curpp.name, "检查月份：%s年%s月" % (curpp.checkdate.year, curpp.checkdate.month), "年龄：%s" % curpp.age]

    curpp.operatorname = request.user.operatorname
    curpp.hospital = request.user.unitname
    form = NotFitCcModifyForm(instance=curpp)
    if request.method == "POST":
        form = NotFitCcModifyForm(request.POST, instance=curpp) # this can modify the current form
        if form.is_valid():
            form.save()
            return notcc_select(request, curpp.id)

    return render_to_response('notcc_applymodify.html', {"form":form, "nomodifyinfo":nomodifyinfo}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def cc_approvallist(request, curid = ""):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curppname = ["姓名", "性别", "区县", "身份证号", "手术时间", "术眼", "联系电话", \
        "手术费用", '基金补助', "是否软晶体", "家庭住址", "审核"]
    curpp     = []

    (curname, curhospital, curisapproval)=("", "", "")
    if curid == "":
        if request.method == 'POST':
            curname         = request.POST['name'].strip()
            curhospital     = request.POST['hospital']
            curisapproval   = request.POST['isapproval']
    else:
        modifypp        = OperationsModel.objects.get(id=curid)
        curname         = modifypp.name
        curhospital     = modifypp.hospital
        curisapproval   = modifypp.isapproval

    request.session['cc_name'] = curname
    request.session['cc_hospital'] = curhospital
    request.session['cc_approval'] = curisapproval
    #=====================new page=================
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPostCounts = int(request.GET.get('allPostCounts',''))
        pageType = str(request.GET.get('pageType', ''))
        get_select_str = str(request.GET.get("get_select_str", "||"))
    except ValueError:
        curPage = 1
        allPostCounts = ""
        pageType = ''
        get_select_str = "||"

    if get_select_str != "||":
        (curname, curhospital, curisapproval) = get_select_str.split("|")
    form = Approval_Cc_SelectForm(initial={'name':curname, 'hospital':curhospital, 'isapproval':curisapproval}) #页面查询窗体
    get_select_str = "|".join([curname, curhospital, curisapproval])

    if curPage < 1:
        curPage = 1
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    startPos = (curPage-1) * MYPAGES
    endPos = startPos + MYPAGES
    cur_re = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, isapproval__icontains=curisapproval).order_by("-operationtime")[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, isapproval__icontains=curisapproval).count()
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
                ipp.phone, ipp.moneytotal, ipp.moneyfund, ipp.softcrystal, ipp.address,], ipp.id, tmpflag])
    
    return render_to_response("cc_approvallist.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage, 'get_select_str':get_select_str},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def cc_approvalinput(request, curid=""):
    '''批准视图'''
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    # 如果为空，则跳转到所有申请表中
    if curid == "":
        return HttpResponseRedirect('/cc_approvallist/')

    # 无论是否审批，都可以随时修改
    try:
        curpp = OperationsModel.objects.get(id=curid)
    except OperationsModel.DoesNotExist:
        return HttpResponseRedirect('/cc_approvallist/')

    nomodifyinfo = ["姓名：%s"  % curpp.name, "手术费用：%s" % curpp.moneytotal, "医院名称：%s" % curpp.hospital, "手术时间：%s" % curpp.operationtime]

    thisday = datetime.date.today()
    jscal_min = (datetime.date(thisday.year, 1, 1).isoformat().replace('-', ''))
    jscal_max = int((thisday + datetime.timedelta(30)).isoformat().replace('-', ''))

    btnname = "修改"
    curpp.approvalman = request.user.operatorname
    if curpp.isapproval != "同意":
        btnname = "审核"
        curpp.approvaldate = thisday
        curpp.isapproval = "同意"
    form = Approval_Cc_Form(instance=curpp)
    if request.method == "POST":
        form = Approval_Cc_Form(request.POST, instance=curpp)
        if form.is_valid():
            savepp = form.save()
            return cc_approvallist(request, savepp.id)
            # return HttpResponseRedirect('/cc_approvallist/') # Redirect
    return render_to_response('cc_approvalinput.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max, "btnname":btnname}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def cc_onekeyapproval(request):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curname         = request.session['cc_name']
    curisapproval   = request.session['cc_approval']
    curhospital     = request.session['cc_hospital']

    today   = datetime.date.today()
    OperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, \
        isapproval__icontains=curisapproval).exclude(isapproval="同意").update(approvalman=request.user.operatorname, moneyfund=1400.00, isapproval="同意", approvaldate=today)

    return cc_approvallist(request, "")

@login_required(login_url="/login/")
def notfit_cc_approvallist(request, curid=""):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curppname = ["姓名", "性别", "区县", "年龄", "医院名称", "联系电话", \
        "手术费用", '基金补助', "不适合手术原因", "医院ID", "月份", "家庭住址", "审核"]
    curpp     = []

    (curname, curhospital, curisapproval)=("", "", "")
    if curid == "":
        if request.method == 'POST':
            curname         = request.POST['name'].strip()
            curhospital     = request.POST['hospital']
            curisapproval   = request.POST['isapproval']
    else:
        modifypp        = NotfitOperationsModel.objects.get(id=curid)
        curname         = modifypp.name
        curhospital     = modifypp.hospital
        curisapproval   = modifypp.isapproval

    request.session['notfitcc_name'] = curname
    request.session['notfitcc_hospital'] = curhospital
    request.session['notfitcc_approval'] = curisapproval
    #=====================new page=================
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPostCounts = int(request.GET.get('allPostCounts',''))
        pageType = str(request.GET.get('pageType', ''))
        get_select_str = str(request.GET.get("get_select_str", "||"))
    except ValueError:
        curPage = 1
        allPostCounts = ""
        pageType = ''
        get_select_str = "||"

    if get_select_str != "||":
        (curname, curhospital, curisapproval) = get_select_str.split("|")
    form = Approval_Cc_SelectForm(initial={'name':curname, 'hospital':curhospital,'isapproval':curisapproval, }) #页面查询窗体
    get_select_str = "|".join([curname, curhospital, curisapproval])

    if curPage < 1:
        curPage = 1
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    startPos = (curPage-1) * MYPAGES
    endPos = startPos + MYPAGES
    cur_re = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, isapproval__icontains=curisapproval).order_by("-checkdate")[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, isapproval__icontains=curisapproval).count()
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
            curpp.append([[ipp.name,ipp.sex,ipp.county,ipp.age,ipp.hospital,\
                ipp.phone,ipp.moneytotal,ipp.moneyfund,ipp.reason,ipp.hospitalID, ipp.checkdate, ipp.address,], ipp.id, tmpflag])
    
    return render_to_response("not_cc_approvallist.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage, 'get_select_str':get_select_str},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def notfit_cc_approvalinput(request, curid=""):
    '''批准视图'''
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    # 如果为空，则跳转到所有申请表中
    if curid == "":
        return HttpResponseRedirect('/notfit_cc_approvallist/')

    try:
        curpp = NotfitOperationsModel.objects.get(id=curid)
    except NotfitOperationsModel.DoesNotExist:
        return HttpResponseRedirect('/notfit_cc_approvallist/')

    nomodifyinfo = ["姓名：%s"  % curpp.name, "检查费用：%s" % curpp.moneytotal, "医院名称:%s" % curpp.hospital, "检查时间：%s" % curpp.checkdate]

    today = datetime.date.today()
    jscal_min = (datetime.date(today.year, 1, 1).isoformat().replace('-', ''))
    jscal_max = int((today + datetime.timedelta(30)).isoformat().replace('-', ''))

    btnname = "修改"
    curpp.approvalman = request.user.operatorname
    if curpp.isapproval != "同意":
        btnname = "审核"
        curpp.approvaldate = today
        curpp.isapproval = "同意"
    form = Approval_Cc_Form(instance=curpp)
    if request.method == "POST":
        form = Approval_Cc_Form(request.POST, instance=curpp)
        if form.is_valid():
            savepp = form.save()
            return notfit_cc_approvallist(request, savepp.id)
    return render_to_response('not_cc_approvalinput.html', {"form":form, "nomodifyinfo":nomodifyinfo,"jscal_min":jscal_min, "jscal_max":jscal_max, "btnname":btnname}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def notfit_cc_onekeyapproval(request):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    curname         = request.session['notfitcc_name']
    curisapproval   = request.session['notfitcc_approval']
    curhospital     = request.session['notfitcc_hospital']

    today   = datetime.date.today()
    cur_re = NotfitOperationsModel.objects.filter(hospital__icontains=curhospital, name__icontains=curname, \
        isapproval__icontains=curisapproval).exclude(isapproval="同意")
    if len(cur_re) != 0:
        for ipp in cur_re:
            if ipp.moneytotal >= 350:
                ipp.moneyfund = 350
            else:
                ipp.moneyfund = ipp.moneytotal
            ipp.approvalman     = request.user.operatorname
            ipp.isapproval      = "同意"
            ipp.approvaldate    = today
            ipp.save()
    
    return notfit_cc_approvallist(request, "")

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
def inituserpassword(request):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    # user = request.user
    form = InitUserPasswordForm()
    if request.method == "POST":
        form = InitUserPasswordForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            newpassword = request.POST['newpassword']            

            user = MyUser.objects.filter(unitsn=username)[0]
            user.set_password(newpassword)
            user.save()
    return render_to_response('changepassword.html', {'form':form,}, context_instance=RequestContext(request))

@login_required(login_url="/login/")
def downloadfile_list(request, unitname="", datayears=""):
    lstauth = [0,1,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    if int(request.user.unitgroup) == 2 or int(request.user.unitgroup) == 1:
        unitname = request.user.unitname #单位名称
        unitreadonly = 1
    else:
        unitname = ""
        unitreadonly = 0

    curppname = ["单位名称", "年份", "更新日期", "文件", "下载"]
    curpp     = []

    if unitname == "":
        if request.method == 'POST':
            unitname    = request.POST['unitname']
            datayears       = request.POST['datayears']
    if unitreadonly == 1:
        unitname = request.user.unitname
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
            downfilename = ipp.filename.encode()
            downfilename = base64.encodebytes(downfilename)
            downfilename = downfilename.decode()
            curpp.append([[ipp.unitname, ipp.datayears,  ipp.updatetime, os.path.basename(ipp.filename),], downfilename])
    
    return render_to_response("download_list.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage, 'unitreadonly':unitreadonly},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def generate_downfiles(request):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    lstresult = jzr.writecsv(BASE_DIR)
    DownloadFilesModel.objects.all().delete()
    for item in lstresult:
        tmpresult = DownloadFilesModel(unitname=item[0], datayears=str(item[1]), filename=item[2], updatetime=item[3])
        tmpresult.save()
    return HttpResponseRedirect("/downloadfile_list/")

@login_required(login_url="/login/")
def downfile_bnz(request, downfilename = ""):
    lstauth = [0,]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')

    if downfilename == "":
        return HttpResponseRedirect("/downloadfile_list/")

    downfilename = downfilename.encode()
    downfilename = base64.decodebytes(downfilename)
    downfilename = downfilename.decode()
    # print(downfilename, os.path.basename(downfilename))

    f = open(downfilename)
    data = f.read()
    f.close()

    response = HttpResponse(data,  content_type='application/x-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % urlquote(os.path.basename(downfilename))
    return response  

def cc_phone(request):
    curppname = ["单位名称", "姓名", "电话", "邮箱"]
    curpp     = []
   
    cur_re = AddressBookModel.objects.all()

    if len(cur_re) != 0:
        for ipp in cur_re:
            curpp.append([ipp.unitname, ipp.name,  ipp.phone, ipp.email,])
    
    return render_to_response("phone_list.html",{'curpp': curpp, 'curppname':curppname, "startPos":0, "allPostCounts":len(cur_re),'allPage':0, 'curPage':0},context_instance=RequestContext(request))  


@login_required(login_url="/login/")
def gmx_list(request, curmonth=""):
    '''光明行视图'''
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    if int(request.user.unitgroup) == 2 or int(request.user.unitgroup) == 1:
        unitname = request.user.unitname #单位名称
    else:
        unitname = ""

    curppname = ["月份", "单位", "当月筛查例数", "当月手术例数", "光明行下乡次数",]
    curpp     = []

    if request.method == 'POST':
        curmonth = request.POST['whichmonth']

    #=====================new page=================
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPostCounts = int(request.GET.get('allPostCounts',''))
        pageType = str(request.GET.get('pageType', ''))
        get_select_str = str(request.GET.get("get_select_str", ""))
    except ValueError:
        curPage = 1
        allPostCounts = ""
        pageType = ''
        get_select_str = ""

    if get_select_str != "":
        curmonth = get_select_str

    form = GMX_Form(initial={'whichmonth':curmonth,}) #页面查询窗体
    get_select_str = curmonth

    if curPage < 1:
        curPage = 1
    #判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    startPos = (curPage-1) * MYPAGES
    endPos = startPos + MYPAGES
    cur_re = GMXModel.objects.filter(whichmonth__icontains=curmonth, unitname__icontains=unitname)[startPos:endPos]
    # posts = BlogPost.objects.all()[startPos:endPos]

    if allPostCounts == "": #标记1
        allPostCounts = GMXModel.objects.filter(whichmonth__icontains=curmonth, unitname__icontains=unitname).count()
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
            curpp.append([ipp.whichmonth, ipp.unitname, ipp.checknums, ipp.operatornums, ipp.gmxnums])
    
    return render_to_response("gmx_list.html",{"form":form, 'curpp': curpp, 'curppname':curppname, "startPos":startPos, "allPostCounts":allPostCounts,'allPage':allPage, 'curPage':curPage, 'get_select_str':get_select_str},context_instance=RequestContext(request))  

@login_required(login_url="/login/")
def gmx_input(request):
    lstauth = [0,2]
    if int(request.user.unitgroup) not in lstauth:
        return render_to_response('noauth.html')
    
    form = GMX_input_Form(initial={'unitname':request.user.unitname})
    if request.method == "POST":
        form = GMX_input_Form(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/gmx_list/")
    return render_to_response('gmx_input.html', {"form":form,}, context_instance=RequestContext(request))