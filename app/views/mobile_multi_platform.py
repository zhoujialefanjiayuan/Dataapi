from datetime import datetime, timedelta, date
from flask import Blueprint, current_app, request
from sqlalchemy import func

from api.advance import nik_multi_platform_from_advance
from api.izidata import nik_multi_platform_from_izidata, mobile_multi_platform_from_izidata
from app.error import INVALID_PARAMETER_ERROR
from app.ext import db
from app.models import Api_order, MobileMultiPlatform
from app.validator import  mobile_multi_platform_validator

mobile_mul_blue = Blueprint("mobile_mul_blue", __name__, url_prefix="/api")
app = current_app


@mobile_mul_blue.route('/mobilemultiplatform', methods=['POST'])
def nik_multi_platform():
    mobilemultiplatformprice = current_app.config.get('MOBILEMULTIPLATFORM')
    params = request.json
    try:
        mobile_multi_platform_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR
    mobile_no = params.get('mobile_no')
    apiorder = Api_order.query.filter(Api_order.name == 'mobilemultiplatform').first().order
    # advance不存在手机多头服务
    #if apiorder == '2':
    # 调用izidata
    if apiorder == '3':
        try:
            re_izi = mobile_multi_platform_from_izidata(mobile_no)['data']
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
                    nikmul = MobileMultiPlatform()
                    nikmul.user = 'yjdhcbhj-inner'
                    nikmul.created_at = datetime.now() - timedelta(days=add_period_time[i])
                    nikmul.mobile_no = mobile_no
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
                'paied': 0 if re_izi['total']==1 else mobilemultiplatformprice
            }
        except:
            print('调用izidata出错')

    # 内部数据库统计
    today = date.today()
    before_90 = today - timedelta(days=90)
    num_everyday = db.session.query(MobileMultiPlatform.day, func.count('id').label('num')).filter(
        MobileMultiPlatform.mobile_no == mobile_no, MobileMultiPlatform.day > before_90).group_by(MobileMultiPlatform.day).all()
    data = {
        "07days": 1,
        "14days": 1,
        "21days": 1,
        "30days": 1,
        "60days": 1,
        "90days": 1,
        "total": 1
    }
    before_7 = today - timedelta(days=7)
    before_14 = today - timedelta(days=14)
    before_21 = today - timedelta(days=21)
    before_30 = today - timedelta(days=30)
    before_60 = today - timedelta(days=60)
    for n in num_everyday:
        print(n.day)
        print(n.num)
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
    data['paied'] = 0 if data['total'] == 1 else mobilemultiplatformprice
    return data