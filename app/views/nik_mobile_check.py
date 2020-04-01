from flask import Blueprint, current_app, request

from api.advance import mobile_nik_check_from_advance
from app.error import INVALID_PARAMETER_ERROR
from app.models import Api_order, NikMobileCheck
from app.validator import nik_mobile_check_validator

nik_mobile_check_blue = Blueprint("nik_mobile_check_blue", __name__, url_prefix="/api")
app = current_app

@nik_mobile_check_blue.route('/nikmobilecheck', methods=['POST'])
def nikmobilecheck():
    nikmobilecheckprice = current_app.config.get('NIKMOBILECHECK')
    params = request.json
    try:
        nik_mobile_check_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR
    mobile_no = params.get('mobile_no')
    nik = params.get('nik')
    #查询本地id
    nikdata = NikMobileCheck.query.filter(NikMobileCheck.nik == nik).scalar()
    if nikdata:
        if  mobile_no == nikdata.mobile_no:
            return {'ismatch':1,'paied':nikmobilecheckprice,'message':''}
    #查询本地mobileNo
    mobiledata = NikMobileCheck.query.filter(NikMobileCheck.mobile_no == mobile_no).scalar()
    if mobiledata:
        if  nik == nikdata.nik:
            return {'ismatch':1,'paied':nikmobilecheckprice,'message':''}

    apiorder = Api_order.query.filter(Api_order.name == 'nikmobilecheck').first().order
    if apiorder == '2':
        # 调用advance服务
        re = mobile_nik_check_from_advance(nik, mobile_no)
        code = re.get('code')
        if code == 'SUCCESS':
            adddata = NikMobileCheck()
            adddata.mobile_no = mobile_no
            adddata.nik = nik
            adddata.add_db_data()
            return {'ismatch': 1, 'paied': nikmobilecheckprice, 'message': ''}
        if code == 'ID_NUMBER_MISMATCHED':
            return {'ismatch': 0, 'paied': nikmobilecheckprice, 'message': "The nik doesn't match the input"}
        if code == 'PHONE_NUMBER_MISMATCHED':
            return {'ismatch': 0, 'paied': nikmobilecheckprice, 'message': "The mobile_no doesn't match the input"}
        if code == 'PHONE_ID_NUMBER_NOT_FOUND':
            return {'ismatch': 0, 'paied': nikmobilecheckprice, 'message': "both input nik and mobile_no can not be found in our system"}
        if code == 'UNSUPPORTED_PHONE_OPERATOR':
            return {'ismatch': 0, 'paied': 0,'message': "this operator are currently unsupported"}
    else:
        return {'ismatch': 0, 'paied': 0, 'message': "this operator are currently unsupported"}
