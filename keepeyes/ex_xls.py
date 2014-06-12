#!/usr/bin/python
# -*- coding: utf-8 -*-

# from  string import zfill as z
import pymysql
import xlrd, datetime, xlwt
import csv
# from tempfile import TemporaryFile

# conn=pymysql.connect(host="218.16.248.155", user="root",passwd="stcl789456",db="kfbnz", use_unicode=1, charset='utf8')
conn=pymysql.connect(host="127.0.0.1", user="root",passwd="stcl789456",db="kfbnz", use_unicode=1, charset='utf8')
xlsfilename  = "D:\yk2013cc.xls"
xlsfilename2  = "D:\yk2013notcc.xls"
# xlsfilename  = "yk2013cc.xls"

def readxlsex2_tmp():
    xlsfilename_04  = r"D:\我的文档\Tencent Files\165222664\FileRecv\1月\1月不适合手术患者名单（上报）.xls"
    strsql = "select name,sex,county,age,hospital,address,phone,\
        moneytotal,moneyfund,reason,hospitalID,checkdate,operatorname,\
        isapproval,approvaldate,approvalman from keepeyes_notfitoperationsmodel"

    thisyear = 2

    cur = conn.cursor()
    # cur.execute(strsql)
    # for r in cur:
    #     print(r)

    # return
    COUNTY_CHOICES = ('金平区','龙湖区','濠江区','澄海区','潮阳区','潮南区','南澳县',)

    sql1 = "insert into keepeyes_notfitoperationsmodel(name,sex,county,age,hospital,address,phone,\
        reason,checkdate,moneytotal,operatorname, isapproval) \
         values(%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s)"
    bk = xlrd.open_workbook(xlsfilename_04)
    totalmoney = 0
    for ish in list(range(0,1)):
        sh = bk.sheets()[ish]
        # print(bk.sheets(), len(bk.sheets()), sh)
        nrows =  sh.nrows        
        checkdate = datetime.date(2014, thisyear, 1) - datetime.timedelta(1)
        for indx in range(5, nrows):
            name            = sh.row(indx)[1].value.strip()
            name            = name.replace(' ', '').replace('　', '')
            if sh.row(indx)[0].value == "" or sh.row(indx)[0].value == "合计":
                # total += indx
                # print(indx, "===============================", sh.name, total, totalmoney)
                break;
            sex             = sh.row(indx)[2].value.strip()
            try:
                age             = int(sh.row(indx)[3].value)
            except:
                age = 60
            address         = sh.row(indx)[4].value.strip()
            county          = address[:3]
            if type(sh.row(indx)[5].value) == type("a"):
                phone = sh.row(indx)[5].value.split("/")[0]
            else:
                phone = str(int(sh.row(indx)[5].value))
            reason          = sh.row(indx)[6].value.strip()
            try:
                moneytotal      = "%.2f" % float(sh.row(indx)[7].value)
            except:
                moneytotal = 0.00
                # print('==============', name, sh.row(indx)[7].value)

            hospital        = "国际眼科中心"
            
            # if type(sh.row(indx)[11].value) == type("a"):
            #     hospitalnumber = sh.row(indx)[11].value
            # else:
            #     hospitalnumber = str(int(sh.row(indx)[11].value))

            operatorname    = "黄丹珊"
            isapproval      = "待审"
            
            totalmoney += float(moneytotal)
            # print(name,sex,county, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,isapproval, approvaldate, approvalman)
            
            tmplstr =(name,sex,county,age,hospital,address,phone,\
                    reason,checkdate,moneytotal,operatorname, isapproval)
            print('------------', name, county)
            if county not in COUNTY_CHOICES:
                print("EEEEEEEEEEEEEEEEEEEEEEEEE", county, sh.name, tmplstr)
                break
                
            # try:
            #     n = cur.execute(sql1,tmplstr)
            #     conn.commit()
            #     # print(sh.name, "OK")
            # except:
            #     print("Error", tmplstr, sh.name)
            #     pass
    print(totalmoney)
    cur.close()

    #    print sh.ncols


def readxlsex2():
    strsql = "select name,sex,county,age,hospital,address,phone,\
        moneytotal,moneyfund,reason,hospitalID,checkdate,operatorname,\
        isapproval,approvaldate,approvalman from keepeyes_notfitoperationsmodel"
    cur = conn.cursor()
    cur.execute(strsql)
    for r in cur:
        print(r)

    # return
    COUNTY_CHOICES = ('金平区','龙湖区','濠江区','澄海区','潮阳区','潮南区','南澳县',)

    sql1 = "insert into keepeyes_notfitoperationsmodel(name,sex,county,age,hospital,address,phone,\
        reason,hospitalID,checkdate,moneytotal,moneyfund,operatorname,\
        isapproval,approvaldate,approvalman) values(%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s, %s, %s)"
    bk = xlrd.open_workbook(xlsfilename2)
    totalmoney = 0
    for ish in list(range(0,12)):
        sh = bk.sheets()[ish]
        # print(bk.sheets(), len(bk.sheets()), sh)
        nrows =  sh.nrows
        if ish == 11:
            checkdate = datetime.date(2013, 12, 31)
        else:
            checkdate = datetime.date(2013, ish+2, 1) - datetime.timedelta(1)
        for indx in range(5, nrows):
            #序号 姓名  性别  年龄  住址  联系电话    不适合手术原因 术前检查费（元）    基金补助金额（元）   ID
            name            = sh.row(indx)[1].value.strip()
            name            = name.replace(' ', '').replace('　', '')
            if name == "":
                # total += indx
                # print(indx, "===============================", sh.name, total, totalmoney)
                break;
            sex             = sh.row(indx)[2].value.strip()
            try:
                age             = int(sh.row(indx)[3].value)
            except:
                age = 60
            address         = sh.row(indx)[4].value.strip()
            county          = address[:3]
            if type(sh.row(indx)[5].value) == type("a"):
                phone = sh.row(indx)[5].value.split("/")[0]
            else:
                phone = str(int(sh.row(indx)[5].value))
            reason          = sh.row(indx)[6].value.strip()
            moneytotal      = "%.2f" % sh.row(indx)[7].value
            moneyfund       = "%.2f" % sh.row(indx)[8].value
            hospitalID      = sh.row(indx)[9].value

            hospital        = "国际眼科中心"
            
            # if type(sh.row(indx)[11].value) == type("a"):
            #     hospitalnumber = sh.row(indx)[11].value
            # else:
            #     hospitalnumber = str(int(sh.row(indx)[11].value))

            operatorname    = "黄丹珊"
            isapproval      = "同意"
            approvaldate    = datetime.date(2014,3,18)
            approvalman     = "iefan"
            totalmoney += float(moneyfund)
            # print(name,sex,county, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,isapproval, approvaldate, approvalman)
            
            tmplstr =(name,sex,county,age,hospital,address,phone,\
                    reason,hospitalID,checkdate,moneytotal,moneyfund,operatorname,\
                    isapproval,approvaldate,approvalman)
            # print('------------', name, moneytotal)
            if county not in COUNTY_CHOICES:
                print("EEEEEEEEEEEEEEEEEEEEEEEEE", county, sh.name, tmplstr)
                break
                
            # try:
            #     n = cur.execute(sql1,tmplstr)
            #     conn.commit()
            #     # print(sh.name, "OK")
            # except:
            #     print("Error", tmplstr, sh.name)
            #     pass
    print(totalmoney)
    cur.close()

    #    print sh.ncols


def readxlsex():
    strsql = "select name,sex,county,ppid,operationtime,hospital,whicheye,address, \
    phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
    isapproval,approvaldate,approvalman from keepeyes_operationsmodel"
    # strsql = "select name,county,hospital from keepeyes_operationsmodel"
    # print(strsql)
    cur = conn.cursor()
    cur.execute(strsql)
    for r in cur:
        print(r)

    # return
    COUNTY_CHOICES = ('金平区','龙湖区','濠江区','澄海区','潮阳区','潮南区','南澳县',)

    sql1 = "insert into keepeyes_operationsmodel(name,sex,county,ppid,operationtime,hospital,whicheye,address, \
        phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
        isapproval,approvaldate,approvalman) values(%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
    bk = xlrd.open_workbook(xlsfilename)
    totalmoney = 0
    for ish in list(range(0,12)):
        sh = bk.sheets()[ish]
        # print(bk.sheets(), len(bk.sheets()), sh)
        nrows =  sh.nrows
        for indx in range(4, nrows):
            #姓名  性别  身份证号    手术时间    手术医院    术眼  家庭住址    联系电话    手术费用（元） 基金补助金额（元）   住院号        
            name            = sh.row(indx)[1].value.strip()
            name            = name.replace(' ', '').replace('　', '')
            if name == "":
                # total += indx
                # print(indx, "===============================", sh.name, total, totalmoney)
                break;
            sex             = sh.row(indx)[2].value.strip()
            ppid            = sh.row(indx)[3].value.strip()
            operationtime   = datetime.date(1899,12,30) + datetime.timedelta(days=int(sh.row(indx)[4].value))
            # hospital        = sh.row(indx)[5].value
            hospital        = "国际眼科中心"
            whicheye        = sh.row(indx)[6].value.strip()
            address         = sh.row(indx)[7].value.strip()
            county          = address[:3]
            
            if type(sh.row(indx)[8].value) == type("a"):
                phone = sh.row(indx)[8].value.split("/")[0]
            else:
                phone = str(int(sh.row(indx)[8].value))
            moneytotal      = "%.2f" % sh.row(indx)[9].value
            moneyfund       = "%.2f" % sh.row(indx)[10].value
            if type(sh.row(indx)[11].value) == type("a"):
                hospitalnumber = sh.row(indx)[11].value
            else:
                hospitalnumber = str(int(sh.row(indx)[11].value))

            softcrystal     = "是"
            operatorname    = "黄丹珊"
            isapproval      = "同意"
            approvaldate    = datetime.date(2014,3,18)
            approvalman     = "iefan"
            totalmoney += float(moneyfund)
            # print(name,sex,county, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,isapproval, approvaldate, approvalman)
            
            tmplstr =(name,sex,county, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,operatorname,isapproval, approvaldate, approvalman)
            if county not in COUNTY_CHOICES:
                print("EEEEEEEEEEEEEEEEEEEEEEEEE", county, sh.name, tmplstr)
                break

            # try:
            #     n = cur.execute(sql1,tmplstr)
            #     conn.commit()
            #     # print(sh.name, "OK")
            # except:
            #     print("Error", tmplstr, sh.name)
            #     pass
    cur.close()

    #    print sh.ncols

def writexlsex():
    cur = conn.cursor()
    lstyear = []
    strsqlmonth0 = "select distinct(YEAR(operationtime)) from keepeyes_operationsmodel"
    cur.execute(strsqlmonth0)
    for iyear in cur:
        lstyear.append(iyear[0])

    fnt = xlwt.Font()
    fnt.name = '宋体'
    # borders = xlwt.Borders()
    # borders.left = xlwt.Borders.THICK
    # borders.right = xlwt.Borders.THICK
    # borders.top = xlwt.Borders.THICK
    # borders.bottom = xlwt.Borders.THICK
    # pattern = xlwt.Pattern()
    # pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    # pattern.pattern_fore_colour = 0x0A
    styledate = xlwt.XFStyle()
    styledate.num_format_str='YYYY-MM-DD'
    otherstyle = xlwt.XFStyle()
    otherstyle.font = fnt
    # style.font = fnt
    # style.borders = borders
    # style.pattern = pattern
    strsql = "select name,sex,county,ppid,operationtime,hospital,whicheye,address, \
        phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
        isapproval,approvaldate,approvalman from keepeyes_operationsmodel "
    lsthead = ["姓名",  "性别", "身份证号", "手术时间", "手术医院", "术眼", "家庭住址", "联系电话", "手术费用（元）","基金补助金额（元）",  "住院号", "是否使用软晶体"]

    for iyear in lstyear:
        for imonth in list(range(1,13)):
            book = xlwt.Workbook(encoding='utf-8')
            strsqltmp = strsql + " where YEAR(operationtime)=%s and MONTH(operationtime)=%i" % (iyear, imonth)
            nn = cur.execute(strsqltmp)
            if nn == 0:
                break

            sheet1 = book.add_sheet(str(imonth) + "月", cell_overwrite_ok=True)
            for ihead in list(range(len(lsthead))):
                sheet1.write(0, ihead, lsthead[ihead])

            indx_row = 1        
            for r in cur:
                (name,sex,county,ppid,operationtime,hospital,whicheye,address, phone,moneytotal,moneyfund,hospitalnumber,softcrystal) = r[:13]
                operatorname = r[13]
                tmplre =(name,sex, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,)

                for icol in list(range(len(tmplre))):
                    if icol == 3:
                        sheet1.write(indx_row, icol, tmplre[icol], styledate)
                    else:
                        sheet1.row(indx_row).write(icol, tmplre[icol],otherstyle)
                indx_row += 1
                
            sheet1.flush_row_data()
            book.save("d:/tmp/%s-%s--%s.xls" % (hospital, iyear, imonth))
    cur.close()

def writecsv():
    cur = conn.cursor()
    lstcounty = []
    sqltmp = "select distinct(county) from keepeyes_operationsmodel"
    cur.execute(sqltmp)
    for icounty in cur:
        lstcounty.append(icounty[0])

    lsthospital = []
    sqltmp = "select distinct(hospital) from keepeyes_operationsmodel"
    cur.execute(sqltmp)
    for ihospital in cur:
        lsthospital.append(ihospital[0])
    lstyear = []
    
    sqltmp = "select distinct(YEAR(operationtime)) from keepeyes_operationsmodel"
    cur.execute(sqltmp)
    for iyear in cur:
        lstyear.append(iyear[0])
    

    strsql = "select name,sex,county,ppid,operationtime,hospital,whicheye,address, \
        phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
        isapproval,approvaldate,approvalman from keepeyes_operationsmodel "
    lsthead = ["姓名",  "性别", "身份证号", "手术时间", "手术医院", "术眼", "家庭住址", "联系电话", "手术费用（元）","基金补助金额（元）",  "住院号", "是否使用软晶体"]

    #医院按年份输出
    for ihospital in lsthospital:
        for iyear in lstyear:
            tmpcsvname = ihospital + "-已做手术-" + str(iyear) + ".csv"
            with open(tmpcsvname, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(lsthead)
                strsqltmp = strsql + " where YEAR(operationtime)=%s order by operationtime" % iyear
                cur.execute(strsqltmp)
                for r in cur:
                    (name,sex,county,ppid,operationtime,hospital,whicheye,address, phone,moneytotal,moneyfund,hospitalnumber,softcrystal) = r[:13]
                    writer.writerow((name,sex,county,"'" + str(ppid),str(operationtime),hospital,whicheye,address, str(phone),"%.2f" % moneytotal,"%.2f" % moneyfund,str(hospitalnumber),softcrystal))

    #区县按年份输出
    for icounty in lstcounty:
        for iyear in lstyear:
            tmpcsvname = icounty + "-已做手术-" + str(iyear) + ".csv"
            with open(tmpcsvname, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(lsthead)
                strsqltmp = strsql + " where YEAR(operationtime)=%s and county='%s'" % (iyear, icounty)
                cur.execute(strsqltmp)
                for r in cur:
                    (name,sex,county,ppid,operationtime,hospital,whicheye,address, phone,moneytotal,moneyfund,hospitalnumber,softcrystal) = r[:13]
                    writer.writerow((name,sex,county,"'" + str(ppid),str(operationtime),hospital,whicheye,address, str(phone),"%.2f" % moneytotal,"%.2f" % moneyfund,str(hospitalnumber),softcrystal))

    cur.close()


def readxlsex_tmp():
    xlsfilename_04  = r"D:\名单\2013\耀辉医院\耀辉医院白内障免费手术汇总表1.xls"
    # xlsfilename_04  = r"D:\我的文档\Tencent Files\165222664\FileRecv\5月\免费手术统计汇总表（5月）.xls"
    strsql = "select name,sex,county,ppid,operationtime,hospital,whicheye,address, \
    phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
    isapproval,approvaldate,approvalman from keepeyes_operationsmodel"
    # strsql = "select name,county,hospital from keepeyes_operationsmodel"
    # print(strsql)
    cur = conn.cursor()
    # cur.execute(strsql)
    # for r in cur:
    #     print(r)

    # return
    COUNTY_CHOICES = ('金平区','龙湖区','濠江区','澄海区','潮阳区','潮南区','南澳县',)

    sql1 = "insert into keepeyes_operationsmodel(name,sex,county,ppid,operationtime,hospital,whicheye,address, \
        phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
        isapproval,approvaldate,approvalman) values(%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
    # sql1 = "insert into keepeyes_operationsmodel(name,sex,county,ppid,operationtime,hospital,whicheye,address, \
    #     phone,moneytotal,hospitalnumber,softcrystal,operatorname, isapproval) \
    #     values(%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s)"
    bk = xlrd.open_workbook(xlsfilename_04)
    totalmoney = 0
    for ish in list(range(0,1)):
        sh = bk.sheets()[ish]
        # print(bk.sheets(), len(bk.sheets()), sh)
        nrows =  sh.nrows
        for indx in range(4, nrows):
            #姓名  性别  身份证号    手术时间    手术医院    术眼  家庭住址    联系电话    手术费用（元） 基金补助金额（元）   住院号        
            name            = sh.row(indx)[1].value.strip()
            name            = name.replace(' ', '').replace('　', '')
            if name == "":
                # total += indx
                # print(indx, "===============================", sh.name, total, totalmoney)
                break;

            print(indx, name)
            sex             = sh.row(indx)[2].value.strip()
            ppid            = sh.row(indx)[3].value.strip()
            operationtime   = datetime.date(1899,12,30) + datetime.timedelta(days=int(sh.row(indx)[4].value))
            # hospital        = sh.row(indx)[5].value
            hospital        = "潮阳耀辉合作医院"
            whicheye        = sh.row(indx)[6].value.strip()
            address         = sh.row(indx)[7].value.strip()
            county          = "潮阳区"
            # county          = address[:3]
            
            if type(sh.row(indx)[8].value) == type("a"):
                phone = sh.row(indx)[8].value.split("/")[0]
            else:
                phone = str(int(sh.row(indx)[8].value))
            moneytotal      = "%.2f" % sh.row(indx)[9].value
            moneyfund       = "%.2f" % sh.row(indx)[10].value
            if type(sh.row(indx)[10].value) == type("a"):
                hospitalnumber = sh.row(indx)[10].value
            else:
                hospitalnumber = str(int(sh.row(indx)[10].value))

            try:
                softcrystal     = sh.row(indx)[11].value
            except:
                softcrystal     = "是"
            operatorname    = "许泽标"
            # operatorname    = "黄丹珊"
            isapproval      = "同意"
            # isapproval      = "待审"
            approvaldate    = datetime.date(2013,12,31)
            approvalman     = "iefan"
            totalmoney += float(moneytotal)
            # print(name,sex,county, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,isapproval, approvaldate, approvalman)
            
            tmplstr =(name,sex,county, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,operatorname,isapproval, approvaldate, approvalman)
            # tmplstr =(name,sex,county, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,hospitalnumber, softcrystal,operatorname, isapproval)
            if county not in COUNTY_CHOICES:
                print("EEEEEEEEEEEEEEEEEEEEEEEEE", county, sh.name, tmplstr)
                break


            # print(tmplstr)
            # try:
            #     # print("========", sql1)
            #     n = cur.execute(sql1,tmplstr)
            #     conn.commit()
            #     # print(sh.name, "OK")
            # except:
            #     print("Error", tmplstr, sh.name)
            #     pass
    print(totalmoney, '========')
    cur.close()

    #    print sh.ncols


def writeXls_CC(downloaddir):
    import pymysql, os, datetime, xlwt
    # downloaddir="downloadfiles/"
    lstresult = []

    conn=pymysql.connect(host="127.0.0.1", user="root",passwd="stcl",db="kfbnz", use_unicode=1, charset='utf8')
    cur = conn.cursor()
    lstcounty = []
    sqltmp = "select distinct(county) from keepeyes_operationsmodel"
    cur.execute(sqltmp)
    for icounty in cur:
        lstcounty.append(icounty[0])

    lsthospital = []
    sqltmp = "select distinct(hospital) from keepeyes_operationsmodel"
    cur.execute(sqltmp)
    for ihospital in cur:
        lsthospital.append(ihospital[0])
        
    lstyear = []
    sqltmp = "select distinct(YEAR(operationtime)) from keepeyes_operationsmodel"
    cur.execute(sqltmp)
    for iyear in cur:
        lstyear.append(iyear[0])

    fnt = xlwt.Font()
    fnt.name = '宋体'
    # borders = xlwt.Borders()
    # borders.left = xlwt.Borders.THICK
    # borders.right = xlwt.Borders.THICK
    # borders.top = xlwt.Borders.THICK
    # borders.bottom = xlwt.Borders.THICK
    # pattern = xlwt.Pattern()
    # pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    # pattern.pattern_fore_colour = 0x0A
    styledate = xlwt.XFStyle()
    styledate.num_format_str='YYYY-MM-DD'
    otherstyle = xlwt.XFStyle()
    otherstyle.font = fnt
    # style.font = fnt
    # style.borders = borders
    # style.pattern = pattern
    

    strsql = "select name,sex,county,ppid,operationtime,hospital,whicheye,address, \
        phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
        isapproval,approvaldate,approvalman from keepeyes_operationsmodel "
    lsthead = ["序号", "姓名",  "性别", "身份证号", "手术时间", "手术医院", "术眼", "家庭住址", "联系电话", "手术费用（元）","基金补助金额（元）",  "住院号", "是否使用软晶体"]

    #医院按月份输出
    today = datetime.date.today()
    for ihospital in lsthospital:
        for iyear in lstyear:
            for imonth in list(range(1,13)):
                strsqltmp = strsql + " where YEAR(operationtime)=%s and MONTH(operationtime)=%i" % (iyear, imonth)
                nn = cur.execute(strsqltmp)
                if nn == 0:
                    break

                book = xlwt.Workbook(encoding='utf-8')
                sheet1 = book.add_sheet(str(imonth) + "月", cell_overwrite_ok=True)
                for ihead in list(range(len(lsthead))):
                    sheet1.write(0, ihead, lsthead[ihead])

                indx_row = 1        
                for r in cur:
                    (name,sex,county,ppid,operationtime,hospital,whicheye,address, phone,moneytotal,moneyfund,hospitalnumber,softcrystal) = r[:13]
                    operatorname = r[13]
                    tmplre =(indx_row, name,sex, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,)

                    for icol in list(range(len(tmplre))):
                        if icol == 4:
                            sheet1.write(indx_row, icol, tmplre[icol], styledate)
                        else:
                            sheet1.row(indx_row).write(icol, tmplre[icol],otherstyle)
                    indx_row += 1
                    
                sheet1.flush_row_data()
                tmpxlsname = ihospital + "-已做手术-" + str(iyear) + "-" + str(imonth).zfill(2) + ".xls"
                tmpxlsname = os.path.join(downloaddir, 'static', 'downloadfiles', tmpxlsname)
                book.save(tmpxlsname)
                lstresult.append([ihospital, iyear, tmpxlsname, today])

    #区县按年份输出
    for icounty in lstcounty:
        for iyear in lstyear:
            strsqltmp = strsql + " where YEAR(operationtime)=%s and county='%s'" % (iyear, icounty)
            n = cur.execute(strsqltmp)
            if n == 0:
                break;

            book = xlwt.Workbook(encoding='utf-8')
            sheet1 = book.add_sheet(str(imonth) + "月", cell_overwrite_ok=True)
            for ihead in list(range(len(lsthead))):
                sheet1.write(0, ihead, lsthead[ihead])

            indx_row = 1
            for r in cur:
                (name,sex,county,ppid,operationtime,hospital,whicheye,address, phone,moneytotal,moneyfund,hospitalnumber,softcrystal) = r[:13]
                tmplre =(indx_row, name,sex, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,)

                for icol in list(range(len(tmplre))):
                    if icol == 4:
                        sheet1.write(indx_row, icol, tmplre[icol], styledate)
                    else:
                        sheet1.row(indx_row).write(icol, tmplre[icol],otherstyle)
                indx_row += 1

            tmpxlsname = icounty + "-已做手术-" + str(iyear) + ".xls"
            tmpxlsname = os.path.join(downloaddir, 'static', 'downloadfiles', tmpxlsname)
            book.save(tmpxlsname)
            lstresult.append([icounty, iyear, tmpxlsname, today])
                
                
    cur.close()
    conn.close()
    return lstresult
if __name__ == '__main__':
    # readxlsex()
    # readxlsex2()
    # readxlsex2_tmp()
    readxlsex_tmp()
    # writexlsex()
    # writeXls_CC("D:/tmp")
    # writecsv()
