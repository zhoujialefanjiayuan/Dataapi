from flask import Blueprint, current_app, request

from api.advance import mobile_auth_from_advance
from app.error import INVALID_PARAMETER_ERROR
from app.models import Api_order, MobileAuth
from app.validator import mobile_online_validator

mobileauthentication_blue = Blueprint("mobileauthentication_blue", __name__, url_prefix="/api")
app = current_app

@mobileauthentication_blue.route('/mobileauthentication', methods=['POST'])
def mobileauthentication():
    mobileauthprice = current_app.config.get('MOBILEAUTH')
    params = request.json
    try:
        mobile_online_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR
    mobile_no = params.get('mobile_no')
    #查询本地
    mobiledata = MobileAuth.query.filter(MobileAuth.mobile_no == mobile_no).scalar()
    if mobiledata:
        if mobiledata.isauth:
            return {'isauth':1,'paied':mobileauthprice,'message':''}
        else:
            return {'isauth': 0, 'paied': mobileauthprice, 'message': 'The phone number is not authenticated'}

    apiorder = Api_order.query.filter(Api_order.name == 'nikmobilecheck').first().order
    if apiorder == '2':
        # 调用advance服务
        re = mobile_auth_from_advance( mobile_no)
        code = re.get('code')
        if code == 'SUCCESS':
            adddata = MobileAuth()
            adddata.mobile_no = mobile_no
            adddata.isauth = True
            adddata.add_db_data()
            return {'isauth': 1, 'paied': mobileauthprice, 'message': ''}
        if code == 'UNAUTHENTICATED_PHONE':
            adddata = MobileAuth()
            adddata.mobile_no = mobile_no
            adddata.isauth = False
            adddata.add_db_data()
            return {'isauth': 0, 'paied': mobileauthprice, 'message': 'The phone number is not authenticated'}
        if code == 'UNSUPPORTED_PHONE_OPERATOR':
            return {'isauth': 0, 'paied': 0,'message': "this operator are currently unsupported"}
    else:
        return {'status':402, 'message': "this operator are currently unsupported"}

