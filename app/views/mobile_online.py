from datetime import datetime

from flask import Blueprint, current_app, request

from api.izidata import mobile_online_from_izidata
from app.error import INVALID_PARAMETER_ERROR
from app.models import Api_order, MobileOnline
from app.validator import mobile_online_validator

mobile_online_blue = Blueprint("mobile_online_blue", __name__, url_prefix="/api")
app = current_app

@mobile_online_blue.route('/mobileonline', methods=['POST'])
def mobileonline():
    mobileonlineprice = current_app.config.get('MOBILEONLINE')
    params = request.json
    try:
        mobile_online_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR
    mobile_no = params.get('mobile_no')
    #调用本地库
    mobileonline_model = MobileOnline.query.filter(MobileOnline.mobile_no == mobile_no).scalar()
    if mobileonline_model:
        age = (datetime.now().year - mobileonline_model.created_at.year)*12 + (datetime.now().month - mobileonline_model.created_at.month)
        age += mobileonline_model.online
        return {'mobile_no':mobile_no,'online':age,'paied':mobileonlineprice}
    else:
        apiorder = Api_order.query.filter(Api_order.name == 'mobileonline').first().order
        if apiorder == '3':
            try:
                re = mobile_online_from_izidata(mobile_no)['data']
                if re:
                    #存储至本地库
                    new = MobileOnline()
                    new.mobile_no = mobile_no
                    new.online = int(re.get('age'))
                    new.add_db_data()
                    return {'mobile_no': mobile_no, 'online': int(re.get('age')),'paied':mobileonlineprice}
            except:
                print('izidata bug')
        return {'status':402,'message':'This phone number can’t be found'}
