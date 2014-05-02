#!/usr/bin/python
# -*- coding: utf-8 -*-

# from  string import zfill as z
import pymysql
import xlrd, datetime, xlwt
from tempfile import TemporaryFile

conn=pymysql.connect(host="127.0.0.1", user="root",passwd="stcl",db="kfbnz", use_unicode=1, charset='utf8')
# xlsfilename  = "D:\yk2013cc.xls"
xlsfilename  = "yk2013cc.xls"
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
    lstmonth = []
    strsqlmonth0 = "select distinct(MONTH(operationtime)) from keepeyes_operationsmodel"
    cur.execute(strsqlmonth0)
    for imonth in cur:
        lstmonth.append(imonth[0])
    # print(lstmonth)
    # return

    # fnt = xlwt.Font()
    # fnt.name = 'Arial'
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
    # style.font = fnt
    # style.borders = borders
    # style.pattern = pattern
    strsql = "select name,sex,county,ppid,operationtime,hospital,whicheye,address, \
        phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
        isapproval,approvaldate,approvalman from keepeyes_operationsmodel "
    lsthead = ["姓名",  "性别", "身份证号", "手术时间", "手术医院", "术眼", "家庭住址", "联系电话", "手术费用（元）","基金补助金额（元）",  "住院号", "是否使用软晶体"]

    for iyear in lstyear:
        book = xlwt.Workbook()
        for imonth in lstmonth:
            strsqltmp = strsql + " where YEAR(operationtime)=%s and MONTH(operationtime)=%i" % (iyear, imonth)
            cur.execute(strsqltmp)

            sheet1 = book.add_sheet(str(imonth) + "月")
            for ihead in list(range(len(lsthead))):
                # print(lsthead[ihead])
                sheet1.write(0, ihead, lsthead[ihead])
            sheet1.flush_row_data()

            indx_row = 1        
            for r in cur:
                (name,sex,county,ppid,operationtime,hospital,whicheye,address, phone,moneytotal,moneyfund,hospitalnumber,softcrystal) = r[:13]
                operatorname = r[13]
                # operationtime = (operationtime - datetime.date(1899, 12, 30)).days
                # datetime.date(1899,12,30) + datetime.timedelta(days=int(sh.row(indx)[4].value))
                tmplre =(name,sex, ppid,operationtime,hospital,whicheye,address,phone,moneytotal,moneyfund,hospitalnumber, softcrystal,)
                for icol in list(range(len(tmplre))):
                    if icol == 3:
                        # print(tmplre[icol], '----------------')
                        sheet1.write(indx_row, icol, tmplre[icol], styledate)
                    else:
                        sheet1.write(indx_row, icol, tmplre[icol])
                indx_row += 1
                print(tmplre)
            sheet1.flush_row_data()

            # print(r[0], r[1], r[4], type(r[4]))

        book.save("ab%s.xls" % iyear)
        book.save(TemporaryFile())
    cur.close()


if __name__ == '__main__':
    # readxlsex()
    writexlsex()
