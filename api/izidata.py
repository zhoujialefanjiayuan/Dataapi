
from api import izi


secretKey=
accessKey=
api = izi.client(accessKey, secretKey)

def parse_response(re):

    if re.get("status") == 'OK':
        if re.get('message') == "PASS":
            return {'data': None, 'channel': 'izidata'}
        else:
            return {'data': re.get('message'),'channel': 'izidata'}
    return IOError

#核黑名单
def vrify_black_from_izidata(nik,mobile_no,name):
    data = {
        "name": str(name),
        "id": str(nik),
        "phone": str(mobile_no)
    }
    response = api.request('https://api.izi.credit/v1/blacklist', data)
    return parse_response(response)

#身份证多头
def nik_multi_platform_from_izidata(nik):
    data = {"id": str(nik)}
    response = api.request('https://api.izi.credit/v1/idinquiries', data)
    print(response)
    return parse_response(response)

#手机号多头
def mobile_multi_platform_from_izidata(mobile_no):
    data = {"phone": str(mobile_no)}
    response = api.request('https://api.izi.credit/v1/phoneinquiries', data)
    print(response)
    return parse_response(response)

#身份检查
def nik_check_from_izidata(nik,name):
    data = {"name": name, "id": str(nik)}
    response = api.request('https://api.izi.credit/v2/identitycheck', data)
    return parse_response(response)

#在网时长
def mobile_online_from_izidata(mobile_no):
    data = {"phone": str(mobile_no)}
    response = api.request('https://api.izi.credit/v2/phoneage', data)
    print(response)
    return parse_response(response)

#充值行为
def mobile_recharge_from_izidata(mobile_no):
    data = {"phone": str(mobile_no)}
    response = api.request('https://api.izi.credit/v1/topup', data)
    print(response)
    return parse_response(response)


if __name__ == '__main__':
    print(mobile_online_from_izidata(6281536186657))

