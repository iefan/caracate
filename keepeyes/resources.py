#coding=utf8
def _getOutCell(outSheet, colIndex, rowIndex):
    """ HACK: Extract the internal xlwt cell representation. """
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row: return None

    cell = row._Row__cells.get(colIndex)
    return cell

def setOutCell(outSheet, col, row, value):
    """ Change cell value without changing formatting. """
    # HACK to retain cell style.
    previousCell = _getOutCell(outSheet, col, row)
    # END HACK, PART I

    outSheet.write(row, col, value)

    # HACK, PART II
    if previousCell:
        newCell = _getOutCell(outSheet, col, row)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx

def writecsv(downloaddir):
    import pymysql, csv, os, datetime
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
    

    strsql = "select name,sex,county,ppid,operationtime,hospital,whicheye,address, \
        phone,moneytotal,moneyfund,hospitalnumber,softcrystal,operatorname, \
        isapproval,approvaldate,approvalman from keepeyes_operationsmodel "
    lsthead = ["姓名",  "性别", "身份证号", "手术时间", "手术医院", "术眼", "家庭住址", "联系电话", "手术费用（元）","基金补助金额（元）",  "住院号", "是否使用软晶体"]

    #医院按年份输出
    today = datetime.date.today()
    for ihospital in lsthospital:
        for iyear in lstyear:
            strsqltmp = strsql + " where YEAR(operationtime)=%s order by operationtime" % iyear
            n = cur.execute(strsqltmp)
            if n != 0:                
                tmpcsvname = ihospital + "-" + str(iyear) + ".csv"
                tmpcsvname = os.path.join(downloaddir, 'keepeyes', 'downloadfiles', tmpcsvname)
                with open(tmpcsvname, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(lsthead)
                    for r in cur:
                        (name,sex,county,ppid,operationtime,hospital,whicheye,address, phone,moneytotal,moneyfund,hospitalnumber,softcrystal) = r[:13]
                        writer.writerow((name,sex,county,"'" + str(ppid),str(operationtime),hospital,whicheye,address, str(phone),"%.2f" % moneytotal,"%.2f" % moneyfund,str(hospitalnumber),softcrystal))
                lstresult.append([ihospital, iyear, tmpcsvname, today])

    #区县按年份输出
    for icounty in lstcounty:
        for iyear in lstyear:
            strsqltmp = strsql + " where YEAR(operationtime)=%s and county='%s'" % (iyear, icounty)
            n = cur.execute(strsqltmp)
            if n!= 0:
                tmpcsvname = icounty + "-" + str(iyear) + ".csv"
                tmpcsvname = os.path.join(downloaddir, 'keepeyes', 'downloadfiles', tmpcsvname)
                with open(tmpcsvname, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(lsthead)
                    for r in cur:
                        (name,sex,county,ppid,operationtime,hospital,whicheye,address, phone,moneytotal,moneyfund,hospitalnumber,softcrystal) = r[:13]
                        writer.writerow((name,sex,county,"'" + str(ppid),str(operationtime),hospital,whicheye,address, str(phone),"%.2f" % moneytotal,"%.2f" % moneyfund,str(hospitalnumber),softcrystal))
                lstresult.append([ihospital, iyear, tmpcsvname, today])

    cur.close()
    conn.close()
    return lstresult

# !!!===!!! MUST NEED ADD 'u' BEFORE IN UNICODE ! ===!!!
UNITGROUP_CHOICES = (\
        ('0', '市残联'),
        ('1', '区残联'),
        ('2', '医院'),
    )
UNITNAMES_CHOICES = (\
    ('国际眼科中心', '国际眼科中心'),
    ('市中心医院', '市中心医院'),
    ('潮阳耀辉合作医院', '潮阳耀辉合作医院'),
    ('潮南民生医院', '潮南民生医院'),
    ('龙湖医院', '龙湖医院'),
    ('濠江医院', '濠江医院'),
    ('澄海人民医院', '澄海人民医院'),
    ('龙湖区第二人民医院', '龙湖区第二人民医院'),
    ('市残联', '市残联'),
    ('金平区残联', '金平区残联'),
    ('龙湖区残联', '龙湖区残联'),
    ('濠江区残联', '濠江区残联'),
    ('澄海区残联', '澄海区残联'),
    ('潮阳区残联', '潮阳区残联'),
    ('潮南区残联', '潮南区残联'),
    ('南澳县残联', '南澳县残联'),
    )

COUNTY_CHOICES = (\
    ('金平区', '金平区'),
    ('龙湖区', '龙湖区'),
    ('濠江区', '濠江区'),
    ('澄海区', '澄海区'),
    ('潮阳区', '潮阳区'),
    ('潮南区', '潮南区'),
    ('南澳县', '南澳县'),
    )
SEX_CHOICES = (\
    ('男', '男'),
    ('女', '女'),
    )
INSU_CHOICES = (\
    ('职工医保','职工医保'),
    ('城乡医保','城乡医保'),
    )
EYE_CHOICES = (\
    ('左眼', '左眼'),
    ('右眼', '右眼'),
    )
HOSPITAL_CHOICES = (\
    ('国际眼科中心', '国际眼科中心'),
    ('市中心医院', '市中心医院'),
    ('潮阳耀辉合作医院', '潮阳耀辉合作医院'),
    ('潮南民生医院', '潮南民生医院'),
    ('龙湖医院', '龙湖医院'),
    ('濠江医院', '濠江医院'),
    ('澄海人民医院', '澄海人民医院'),
    ('龙湖区第二人民医院', '龙湖区第二人民医院'),
    )
ISAPPROVAL_CHOICES = (\
    ('同意', '同意'),
    ('作废', '作废'),
    ('退审', '退审'),
    )
SAVEOK_CHOICES = (\
    ('已确认', '已确认'),
    ('过期', '过期'),
    )
ISCAL_CHOICES = (\
    ('已结算','已结算'),
    ('待结算','待结算'),
    )
YESNO_CHOICE = (\
    ('是','是'),
    ('否','否'),
    )
YESNO01_CHOICE = (\
    ('','--'),
    ('0','是'),
    ('1','否'),
    )