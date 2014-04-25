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
ECON_CHOICES = (\
    ('低保', '低保'),
    ('五保', '五保'),
    ('特困', '特困'),
    ('困难', '困难'),
    )
CITY_CHOICE = (\
    ('非农', '非农'), 
    ('农村', '农村'),
    )
RELASHIP_CHOICES = (\
    ('配偶','配偶'),
    ('子女','子女'),
    ('孙子女','孙子女'),
    ('父母','父母'),
    ('祖父母','祖父母'),
    ('兄弟姐妹','兄弟姐妹'),
    ('其他','其他'),
    )
DISLEVEL_CHOICES = (\
    ("61", "61"),
    ("62", "62"),
    ("63", "63"),
    ("64", "64"),
    ('其他','其他'),
    )
INSU_CHOICES = (\
    ('职工医保','职工医保'),
    ('城乡医保','城乡医保'),
    )

CERT1_CHOICES = (\
    ('身份证','身份证'), 
    ('户口本','户口本'),
    )
CERT2_CHOICES = (\
    ('精神残疾证','精神残疾证'), 
    ('精神障碍诊断证明','精神障碍诊断证明'),
    ('非精神残疾证', '非精神残疾证'),
    )
CERT3_CHOICES = (\
    ('低保证','低保证'),
    ('五保证','五保证'),
    ('特困证','特困证'),
    ('困难证明','困难证明'),
    )
HOSPITAL_CHOICES = (\
    ('市四本部', '市四本部'),
    ('礐石', '礐石'),
    ('红莲池', '红莲池'),
    ('汕大', '汕大'),
    )
PERIOD_CHOICES = (\
    ('急性','急性'),
    ('慢性','慢性'),
    )
CONTINUE_CHOICES = (\
    ('间隔救助', '间隔救助'),
    ('续院救助', '续院救助'),
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