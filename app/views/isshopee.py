#高频访问，建议ip代理
from flask import Blueprint, current_app, request

from app.error import INVALID_PARAMETER_ERROR
from app.validator import mobile_online_validator

import requests

def isshopee(mobile_no):
    url = 'https://shopee.co.id/api/v2/authentication/login'
    data = {'password': "a1a2151803e29910638937813ebc71e700432ed4080de02889aec72b381551e5".replace('9',mobile_no[5]),
            'captcha': "",
            'support_whats_app': True,
            'phone': str(mobile_no)}

    headers = {
        'cookie': '_gcl_au=1.1.1333444028.1584353565; _med=refer; _fbp=fb.2.1584353566719.1716391114; SPC_IA=-1; SPC_EC=-; SPC_U=-; SPC_F=mbjcT02L1REOlXyeeb8WHWenxzqXSTK5; REC_T_ID=b03696a2-676e-11ea-a0f1-ccbbfe27d9cf; SPC_SI=ch2qym13fmqf3xrbple71592u7gznhde; REC_T_ID=b048ab25-676e-11ea-8aca-3c15fb7e9df9; _ga=GA1.3.382742654.1584353570; _gid=GA1.3.495086122.1584353570; G_ENABLED_IDPS=google; AMP_TOKEN=%24NOT_FOUND; csrftoken=m1aVO2JjjGiLgKpmYDXvprgwqVeYTNI4; _dc_gtm_UA-61904553-8=1; REC_MD_20=1584498927; REC_MD_30_2001204858=1584499465; SPC_R_T_ID="ehLVPbUvgMFKAQsEbabuWxyLEn5z9+0I/nvsi7N7sjwRcX5Wdrs52q/rek9vmW9XXG+RbM8j3Ov2Rqz+Tmd2WWZS0Vd1i8LBqx1UXmP3AfA="; SPC_T_IV="p4K39XnI5I9h69M/h7TowQ=="; SPC_R_T_IV="p4K39XnI5I9h69M/h7TowQ=="; SPC_T_ID="ehLVPbUvgMFKAQsEbabuWxyLEn5z9+0I/nvsi7N7sjwRcX5Wdrs52q/rek9vmW9XXG+RbM8j3Ov2Rqz+Tmd2WWZS0Vd1i8LBqx1UXmP3AfA=',
        'if-none-match-': '55b03-78cdb99dd963307b576f027c43718238',
        'origin': 'https://shopee.co.id',
        'referer': 'https://shopee.co.id/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'x-api-source': 'pc',
        'x-csrftoken': 'm1aVO2JjjGiLgKpmYDXvprgwqVeYTNI4',
        'x-requested-with': 'XMLHttpRequest'}
    re = requests.post(url, json=data,headers=headers).json()
    if re.get('error') == 4:
        return False
    else:
        return True



isshopee_blue = Blueprint("isshopee_blue", __name__, url_prefix="/api")


@isshopee_blue.route('/isshopee', methods=['POST'])
def isshopee_check():
    isshopeeprice = current_app.config.get('ISSHOPEE')
    params = request.json
    try:
        mobile_online_validator(params)
    except Exception as e:
        INVALID_PARAMETER_ERROR['message'] = str(e)
        return INVALID_PARAMETER_ERROR
    mobile_no = params.get('mobile_no')
    re = isshopee(mobile_no)
    return {'isshopee':re,'paied':isshopeeprice}




