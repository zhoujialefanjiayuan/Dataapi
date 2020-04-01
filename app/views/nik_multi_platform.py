from datetime import datetime, timedelta, date
from flask import Blueprint, current_app, request
from sqlalchemy import func

from api.advance import nik_multi_platform_from_advance
from api.izidata import nik_multi_platform_from_izidata
from app.error import INVALID_PARAMETER_ERROR
from app.ext import db
from app.models import Api_order, NikMultiPlatform
from app.validator import nik_multi_platform_validator

nik_mul_blue = Blueprint("nik_mul_blue", __name__, url_prefix="/api")
app = current_app


@nik_mul_blue.route('/nikmultiplatform', methods=['POST'])
def nik_multi_platform():
    nikmultiplatformprice = current_app.config.get('NIKMULTIPLATFORM')
    params = request.json
    try:
        nik_multi_platform_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR
    nik = params.get('nik')
    apiorder = Api_order.query.filter(Api_order.name == 'nikmultiplatform').first().order
    # 调用advance
    if apiorder == '2':
        try:
            re_adv = nik_multi_platform_from_advance(nik)
            if re_adv:
                p_c = re_adv["statisticCustomerInfo"]
                day_count = [i['queryCount'] for i in p_c]
                day_count.sort(reverse=True)
                add_period_count = []
                for i in range(0, len(day_count) - 1):
                    add_period_count.append(day_count[i] - day_count[i + 1])
                add_period_time = [66, 38, 22, 16, 3]
                for i in range(5):
                    if add_period_count[i] == 0:
                        continue
                    else:
                        # 存储多头数据
                        nikmul = NikMultiPlatform()
                        nikmul.user = 'yjdhcbhj-inner'
                        nikmul.created_at = datetime.now() - timedelta(days=add_period_time[i])
                        nikmul.nik = nik
                        nikmul.channel = 'advance'
                        db.session.add(nikmul)
                db.session.commit()
                return {
                    "07days": p_c[0]['queryCount'],
                    "14days":  p_c[1]['queryCount'],
                    "21days":  p_c[2]['queryCount'],
                    "30days":  p_c[3]['queryCount'],
                    "60days":  p_c[4]['queryCount'],
                    "90days":  p_c[5]['queryCount'],
                    "total":  sum(day_count),
                    'paied': nikmultiplatformprice
                }

            else:
                return {
                    "07days": 0,
                    "14days": 0,
                    "21days": 0,
                    "30days": 0,
                    "60days": 0,
                    "90days": 0,
                    "total":0,
                    'paied': 0
                }
        except:
            print()
    # 调用izidata
    if apiorder == '3':
        try:
            re_izi = nik_multi_platform_from_izidata(nik)['data']
            print(re_izi)
            days_count = list(re_izi.values())
            days_count.sort(reverse=True)
            days_count = days_count[1:]
            add_period_count = []
            for i in range(0, len(days_count) - 1):
                add_period_count.append(days_count[i] - days_count[i + 1])
            add_period_time = [66, 38, 22, 16, 3]
            for i in range(5):
                if add_period_count[i] == 0:
                    continue
                else:
                    # 存储多头数据
                    nikmul = NikMultiPlatform()
                    nikmul.user = 'yjdhcbhj-inner'
                    nikmul.created_at = datetime.now() - timedelta(days=add_period_time[i])
                    nikmul.nik = nik
                    nikmul.channel = 'izidata'
                    db.session.add(nikmul)
            db.session.commit()
            return {
                "07days": re_izi['07d'],
                "14days": re_izi['14d'],
                "21days": re_izi['21d'],
                "30days": re_izi['30d'],
                "60days": re_izi['60d'],
                "90days": re_izi['90d'],
                "total": re_izi['total'],
                'paied': 0 if re_izi['total']==1 else nikmultiplatformprice
            }
        except:
            print('调用izidata出错')

    #内部数据库统计
    today = date.today()
    before_90 = today - timedelta(days=90)
    num_everyday = db.session.query(NikMultiPlatform.day, func.count('id').label('num')).filter(
        NikMultiPlatform.nik == nik, NikMultiPlatform.day > before_90).group_by(
        NikMultiPlatform.day).all()
    data = {
        "07days": 0,
        "14days": 0,
        "21days": 0,
        "30days": 0,
        "60days": 0,
        "90days": 0,
        "total":0
    }
    before_7 = today - timedelta(days=7)
    before_14 = today - timedelta(days=14)
    before_21 = today - timedelta(days=21)
    before_30 = today - timedelta(days=30)
    before_60 = today - timedelta(days=60)
    for n in num_everyday:
        data['total'] += n.num
        if n.day > before_7:
            data['90days'] += n.num
            data['60days'] += n.num
            data['30days'] += n.num
            data['21days'] += n.num
            data['14days'] += n.num
            data['07days'] += n.num
            continue
        if n.day > before_14:
            data['90days'] += n.num
            data['60days'] += n.num
            data['30days'] += n.num
            data['21days'] += n.num
            data['14days'] += n.num
            continue
        if n.day > before_21:
            data['90days'] += n.num
            data['60days'] += n.num
            data['30days'] += n.num
            data['21days'] += n.num
            continue
        if n.day > before_30:
            data['90days'] += n.num
            data['60days'] += n.num
            data['30days'] += n.num
            continue
        if n.day > before_60:
            data['90days'] += n.num
            data['60days'] += n.num
            continue
        data['90days'] += n.num
    data['paied'] = 0 if data['total'] == 1 else nikmultiplatformprice
    return data