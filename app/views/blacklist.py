import json

from flask import Blueprint, request,current_app

from api.advance import vrify_black_from_advance
from api.hadu import vrify_black_from_hadu
from api.izidata import vrify_black_from_izidata
from app.error import INVALID_PARAMETER_ERROR
from app.ext import db
from app.models import Black_list, Api_order
from app.validator import checkblack_validator

black_blue  = Blueprint("black_blue", __name__,url_prefix="/api")


@black_blue.route('/checkblack',methods=['POST'])
def checkblack():
    checkblackprice = current_app.config.get('CHECKBLACK')
    params = request.json
    try:
        checkblack_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR


    nik = params.get('nik')
    mobile_no = params.get('mobile_no')
    name = params.get('name')
    black_nik = Black_list.query.filter(Black_list.nik == nik).all()
    #先查内部库nik
    if black_nik:
        #如果nik存在，mobile_no不存在，存储入库
        if not Black_list.query.filter(Black_list.nik == nik,Black_list.mobile_no == mobile_no,).all():
            black_obj = Black_list()
            black_obj.hitReason = black_nik[0].hitReason
            black_obj.nik = nik
            black_obj.mobile_no = mobile_no
            black_obj.name = name
            black_obj.channel = 'inner'
            black_obj.eventtime = black_nik[0].eventtime
            black_obj.response = ''
            db.session.add(black_obj)
            db.session.commit()
        return {'isblack':1,
                "reason":black_nik[0].hitReason,
                'blacktime':black_nik[0].eventtime,
                'paied':checkblackprice}
    else:
        #查内部库mobile,若查出，添加nik
        black_mobile = Black_list.query.filter(Black_list.mobile_no == mobile_no).all()
        if black_mobile:
            # 如果mobile_no存在，nik不存在，存储入库
            if not Black_list.query.filter(Black_list.nik == nik, Black_list.mobile_no == mobile_no, ).all():
                black_obj = Black_list()
                black_obj.hitReason = black_mobile[0].hitReason
                black_obj.nik = nik
                black_obj.mobile_no = mobile_no
                black_obj.name = name
                black_obj.channel = 'inner'
                black_obj.eventtime = black_mobile[0].eventtime
                black_obj.response = ''
                db.session.add(black_obj)
                db.session.commit()
            return {'isblack':1,
                "reason":black_mobile[0].hitReason,
                'blacktime':black_mobile[0].eventtime,
                    'paied':checkblackprice}
        else:
            #查询第三方接口数据库
            apiorder = Api_order.query.filter(Api_order.name == 'checkblack').first().order
            for i in apiorder.split(','):
                #调用哈杜
                if i == '1':
                    try:
                        hadu_response = vrify_black_from_hadu(**params)
                        print(hadu_response)
                        if hadu_response['Code'] == 200:
                            if hadu_response['Hits']['Blacklist'] == 1:
                                reason = hadu_response['Result'][0]["BlackLevel"]
                                oldblacktime = hadu_response['Result'][0]["BlackTime"]
                                black_obj= Black_list()
                                black_obj.hitReason = reason
                                black_obj.nik = nik
                                black_obj.mobile_no = mobile_no
                                black_obj.name = name
                                black_obj.channel = 'hadu'
                                black_obj.eventtime = oldblacktime
                                black_obj.response = json.dumps(hadu_response)
                                db.session.add(black_obj)
                                db.session.commit()
                                return {'isblack': 1,
                                        "reason":reason,
                                        'blacktime': oldblacktime,
                                        'paied':checkblackprice}
                    except:
                        print('hadu bug')
                #调用advance
                if i == '2':
                    try:
                        advance_response = vrify_black_from_advance(**params)
                        print(advance_response)
                        if advance_response['data']:
                            reject_result = advance_response['data']['defaultListResult'][0]
                            black_obj = Black_list()
                            black_obj.hitReason = reject_result["reasonCode"]
                            black_obj.nik = nik
                            black_obj.mobile_no = mobile_no
                            black_obj.name = name
                            black_obj.channel = 'advance'
                            black_obj.eventtime =reject_result["eventTime"]
                            black_obj.response = json.dumps(advance_response)
                            db.session.add(black_obj)
                            db.session.commit()
                            return {'isblack': 1,
                                    "reason": reject_result["reasonCode"],
                                    'blacktime': reject_result["eventTime"],
                                    'paied':checkblackprice}
                    except:
                        print('advance bug')
                #调用izidata
                if i == '3':
                    try:
                        izidata_response = vrify_black_from_izidata(**params)
                        print(izidata_response)
                        if izidata_response['data']:
                            black_obj = Black_list()
                            black_obj.reason = ''
                            black_obj.nik = nik
                            black_obj.mobile_no = mobile_no
                            black_obj.name = name
                            black_obj.channel = 'izidata'
                            black_obj.eventtime = '01/2018'
                            black_obj.response = json.dumps(izidata_response)
                            db.session.add(black_obj)
                            db.session.commit()
                            return {'isblack': 1,
                                    "reason": 'OVERDUE_DAYS_BETWEEN_60_TO_90',
                                    'blacktime': '01/2018',
                                    'paied':checkblackprice}
                    except:
                        print('izidata bug')
            return {'isblack': 0,
                    "reason": "",
                    'blacktime': "",
                    'paied':0}



