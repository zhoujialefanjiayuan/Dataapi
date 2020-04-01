from flask import Blueprint, current_app, request

from api.advance import nik_check_from_advance
from api.izidata import nik_check_from_izidata
from app.error import INVALID_PARAMETER_ERROR
from app.models import Api_order, NIkCheck
from app.validator import nik_check_validator

nik_check_blue = Blueprint("nik_check_blue", __name__, url_prefix="/api")
app = current_app

@nik_check_blue.route('/nikcheck', methods=['POST'])
def nik_check():
    nikcheckprice = current_app.config.get('NIKCHECK')
    params = request.json
    try:
        nik_check_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR
    nik = params.get('nik')
    name = params.get('name').upper()
    birth_year = ('20'+nik[10:12]) if int(nik[10:12]) < 25 else ('19'+ nik[10:12])
    birth = (('0' + nik[7]) if int(nik[6]) > 3 else nik[6:8]) + '-' + nik[8:10] + '-' + birth_year

    #查询内部库
    nikdata = NIkCheck.query.filter(NIkCheck.nik == nik).first()
    if nikdata:
        data = {
                "nik": nikdata.nik,
                "name":nikdata.name ,
                "date_of_birth": nikdata.date_of_birth,
                "age":2020 - int(birth_year),
                "gender": nikdata.gender,
                "address":nikdata.address,
                "province": nikdata.province,
                "city": nikdata.city,
                "district": nikdata.district,
                "village": nikdata.village,
                "religion": nikdata.religion,
                "marital_status": nikdata.marital_status,
                "work": nikdata.work,
                "istrue":1 if nikdata.name == name else 0,
                "paied":nikcheckprice
              }
        return data
    #调用第三方服务
    else:
        apiorder = Api_order.query.filter(Api_order.name == 'nikcheck').first().order.split(',')
        print(apiorder)
        for theorder in apiorder:
            #advance
            if theorder == '2':
                try:
                    re = nik_check_from_advance(nik,name)
                    if re:
                        data = {
                            "nik": nik,
                            "name": re.get('name'),
                            "date_of_birth": birth,
                            "gender": '',
                            "address": '',
                            "province": re.get('province'),
                            "city": re.get("city"),
                            "district": re.get("district"),
                            "village": re.get("village"),
                            "religion": '',
                            "marital_status": '',
                            "work": '',
                            "age":2020 - int(birth_year),
                            "istrue": 1 if  re.get('name') == name else 0,
                            "paied": nikcheckprice
                        }
                        #存储至本地
                        nikcheck = NIkCheck()
                        nikcheck.nik = nik
                        nikcheck.channel = 'advance'
                        nikcheck.name = re.get('name')
                        nikcheck.province = re.get('province')
                        nikcheck.city = re.get('city')
                        nikcheck.district = re.get('district')
                        nikcheck.village = re.get('village')
                        nikcheck.date_of_birth = birth
                        nikcheck.add_db_data()
                        return data
                except:
                    print('advance bug')
            #izidata
            if theorder == '3':
                try:
                    re = nik_check_from_izidata(nik,name).get('data')
                    if re:
                        data = {
                            "nik": nik,
                            "name": re.get('name'),
                            "date_of_birth": birth,
                            "gender": re.get('gender',''),
                            "address": re.get('address',''),
                            "province": re.get('province'),
                            "city": re.get("city"),
                            "district": re.get("district"),
                            "village": re.get("village"),
                            "religion": re.get('religion',''),
                            "marital_status":re.get('marital_status',''),
                            "work": re.get('work',''),
                            "age": 2020 - int(birth_year),
                            "istrue": 1 if re.get('name') == name else 0,
                            "paied": nikcheckprice
                        }
                        # 存储至本地
                        nikcheck = NIkCheck()
                        nikcheck.nik = nik
                        nikcheck.channel = 'izidata'
                        nikcheck.gender = re.get('gender','')
                        nikcheck.address = re.get('address','')
                        nikcheck.religion = re.get('religion','')
                        nikcheck.marital_status = re.get('marital_status','')
                        nikcheck.work = re.get('work','')
                        nikcheck.name = re.get('name')
                        nikcheck.province = re.get('province')
                        nikcheck.city = re.get('city')
                        nikcheck.district = re.get('district')
                        nikcheck.village = re.get('village')
                        nikcheck.date_of_birth = birth
                        nikcheck.add_db_data()
                        return data
                except:
                    print('izidata bug')
        return {"status": 402,"message": "person not found"}








