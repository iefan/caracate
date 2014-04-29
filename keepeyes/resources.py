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
    ('待审', '待审'),
    ('退审', '退审'),
    ('同意', '同意'),
    ('作废', '作废'),
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