from api.http_client_advance import OpenApiClient

def parse_response(re):
    print('advance',re)
    if re.get('code') == "SUCCESS":
        if re.get('pricingStrategy') == "FREE":
            return {'data':None,'channel':'advance'}
        else:
            return {'data':re.get('data'),'channel':'advance'}
    return IOError


#黑名单
def vrify_black_from_advance(nik,mobile_no,name):
    data = {
    "name":str(name),
    "idNumber":str(nik),
    "phoneNumber":{
         "countryCode": "+62",
         "areaCode": "",
         "number": str(mobile_no)[3:]
        }
    }
    re = advancd_request.request('/openapi/anti-fraud/v5/blacklist-check',data)
    return parse_response(re)


def nik_multi_platform_from_advance(nik):
    data = {
            "idNumber":str(nik)
        }
    re = advancd_request.request('/openapi/verification/v6/multi-platform',data)
    return re.get('data')

def nik_check_from_advance(nik,name):
    data = {
            "idNumber":str(nik),
            "name":str(name)
        }
    re = advancd_request.request('/openapi/anti-fraud/v4/identity-check',data)
    print(re)
    return re.get('data')


#电信id检查
def mobile_nik_check_from_advance(nik,mobile_no):
    data = {
        "idNumber":str(nik),
        "phoneNumber":{
               "countryCode": "+62",
               "areaCode": "",
               "number": str(mobile_no)[3:]
          }
    }
    re = advancd_request.request('/openapi/operator/v1/tele-identity-check', data)
    return re


#手机号认证
def mobile_auth_from_advance(mobile_no):
    data = {
        "phoneNumber":{
               "countryCode": "+62",
               "areaCode": "",
               "number": str(mobile_no)[3:]
          }
    }
    re = advancd_request.request('/openapi/operator/v1/tele-authentication', data)
    return re

if __name__ == '__main__':
    print(mobile_nik_check_from_advance("3216051605940007","+6281291465680"))
