
from flask import Blueprint, current_app, request

from api.izidata import mobile_recharge_from_izidata
from app.error import INVALID_PARAMETER_ERROR
from app.models import Api_order, MobileRecharge
from app.validator import mobile_online_validator

mobilerecharge_blue = Blueprint("mobilerecharge_blue", __name__, url_prefix="/api")



def dict_to_str(di):
    return '-'.join([str(di['avg']), str(di['times']), str(di['max']),str(di['min'])])

def str_to_dict(ss):
    allvalues = ss.split('-')
    return {
      "avg": int(allvalues[0]),
      "times": int(allvalues[1]),
      "max": int(allvalues[2]),
      "min": int(allvalues[3])
    }


@mobilerecharge_blue.route('/mobilerecharge', methods=['POST'])
def mobileonline():
    mobilerechargeprice = current_app.config.get('MOBILERECHARGE')
    params = request.json
    try:
        mobile_online_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR
    mobile_no = params.get('mobile_no')
    # 调用本地库
    mobileonline_model = MobileRecharge.query.filter(MobileRecharge.mobile_no == mobile_no).scalar()
    if mobileonline_model:
        senddata = {}
        senddata['topup_0_30'] = str_to_dict(mobileonline_model.topup_0_30)
        senddata['topup_0_60'] = str_to_dict(mobileonline_model.topup_0_60)
        senddata['topup_0_90'] = str_to_dict(mobileonline_model.topup_0_90)
        senddata['topup_0_180'] = str_to_dict(mobileonline_model.topup_0_180)
        senddata['topup_0_360'] = str_to_dict(mobileonline_model.topup_0_360)
        senddata['topup_30_60'] = str_to_dict(mobileonline_model.topup_30_60)
        senddata['topup_60_90'] = str_to_dict(mobileonline_model.topup_60_90)
        senddata['topup_90_180'] = str_to_dict(mobileonline_model.topup_90_180)
        senddata['topup_180_360'] = str_to_dict(mobileonline_model.topup_180_360)
        senddata['topup_360_720'] = str_to_dict(mobileonline_model.topup_360_720)
        senddata['mobile_no'] = mobile_no
        senddata['paied'] = mobilerechargeprice
        return senddata
    else:
        apiorder = Api_order.query.filter(Api_order.name == 'mobilerecharge').first().order
        if apiorder == '3':
            try:
                re = mobile_recharge_from_izidata(mobile_no)['data']
                if re:
                    adddata = MobileRecharge()
                    adddata.mobile_no = mobile_no
                    adddata.topup_0_30 = dict_to_str(re.get('topup_0_30'))
                    adddata.topup_0_60 = dict_to_str(re.get('topup_0_60'))
                    adddata.topup_0_90 = dict_to_str(re.get('topup_0_90'))
                    adddata.topup_0_180 = dict_to_str(re.get('topup_0_180'))
                    adddata.topup_0_360 = dict_to_str(re.get('topup_0_360'))
                    adddata.topup_30_60 = dict_to_str(re.get('topup_30_60'))
                    adddata.topup_60_90 = dict_to_str(re.get('topup_60_90'))
                    adddata.topup_90_180 = dict_to_str(re.get('topup_90_180'))
                    adddata.topup_180_360 = dict_to_str(re.get('topup_180_360'))
                    adddata.topup_360_720 = dict_to_str(re.get('topup_360_720'))
                    adddata.add_db_data()
                    re['mobile_no'] = mobile_no
                    re['paied'] = mobilerechargeprice
                    return re
            except:
                print('izidata not found')
    return {'status': 402, 'message': "This phone number can’t be found"}
