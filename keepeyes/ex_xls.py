#!/usr/bin/python
# -*- coding: utf-8 -*-

# from  string import zfill as z
import pymysql
import xlrd

conn=pymysql.connect(host="127.0.0.1", user="root",passwd="stcl",db="kfbnz", use_unicode=1, charset='utf8')
xlsfilename  = "D:\yk2013cc.xls"
def readxlsex():
    addr_dict = {}
    strsql = "select name,sex,county,ppid,operationtime,hospital,whicheye,address, \
    phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
    isapproval,approvaldate,approvalman from keepeyes_operationsmodel"
    # strsql = "select name,county,hospital from keepeyes_operationsmodel"
    print(strsql)
    cur = conn.cursor()
    cur.execute(strsql)
    for r in cur:
        print(r)

    return

    sql1 = "insert into edu_student(name, sex, years, birth, addrsn, stu_id, stu_class, stu_school, stu_startyear, stu_schoolyears, family_relation, family_member_name, family_member_id, money_nums, phone) values(%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s, %s, %s, %s, %s)"
    xlsfilename  = "D:\workdb\zulian\student2.xls"
    bk = xlrd.open_workbook(xlsfilename)
    sh = bk.sheets()[0]
    nrows =  sh.nrows
    tmplststudent = ()
    lststuclass = []
    lstclass0 = [u"小", u"特"]
    lstclass1 = [u"初"]
    lstclass2 = [u"中", u"高"]
    lstclass3 = [u"专"]
    lstclass4 = [u"本"]
    lstclass5 = [u"研"]
    for indx in range(1, nrows):
        name          = sh.row(indx)[1].value
        sex              = sh.row(indx)[2].value
        stu_id           = sh.row(indx)[3].value
        stu_school       = sh.row(indx)[4].value
        school_startyear      = int(sh.row(indx)[5].value)
        stu_class        = sh.row(indx)[6].value
        addr_name        = addr_dict[sh.row(indx)[7].value[:2]]
        family_name      = sh.row(indx)[8].value
        family_id        = sh.row(indx)[9].value
        get_money        = int(sh.row(indx)[10].value)
        phone            = sh.row(indx)[11].value


        if stu_class[0] in lstclass0:
            stu_class = u"小学"
        elif stu_class[0] in lstclass1:
            stu_class = u"初中"
        elif stu_class[0] in lstclass2:
            stu_class = u"高中｜中专｜技工"
        elif stu_class[0] in lstclass3:
            stu_class = u"大专"
        elif stu_class[0] in lstclass4:
            stu_class = u"本科"
        elif stu_class[0] in lstclass5:
            stu_class = u"研究生"

        # if birth[0] == 'u':
        #     birth = birth[2:-1]
        # if birth == "''":
        #     birth = ''
        name = name.replace(' ', '')
        name = name.replace(u'　', '')
        tmplststudent = (name, sex, '2012', '', addr_name, stu_id, stu_class, stu_school, school_startyear, '', '', family_name, family_id, get_money, phone)

        try:
            n = cur.execute(sql1,tmplststudent)
        except:
            # print addr_name, name
            pass

#    print sh.ncols


if __name__ == '__main__':
    readxlsex()
