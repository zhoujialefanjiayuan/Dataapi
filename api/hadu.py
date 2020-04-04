import hashlib
import hmac
import json
import time
import requests

from app.error import RETRY_LATER



def signRequest(algorithm, secret, timestamp, httpMethod, originalUrl, httpBody):
  '''
  Sign HTTP Request
  :param str  algorithm   : HMAC algorithm, currently only sha256
  :param str  secret      : your secret
  :param str  timestamp   : current unix timestamp (second)
  :param str  httpMethod  : upper case http method like GET
  :param str  originalUrl : original url without host like /api/path?params
  :param dict httpBody    : request body dict (allow null)
  :return: hex signature
  :rtype: str
  '''
  hm = hmac.new(secret.encode('utf-8'), digestmod=algorithm)

  hm.update(timestamp.encode('utf-8')) # add timestamp provided in header to make sure it hasn't been changed
  hm.update(httpMethod.encode('utf-8')) # add verb e.g POST, GET
  hm.update(originalUrl.encode('utf-8')) # add url e.g /api/order?id=1

  # if we have a request body, create a md5 hash of it and add it to the hmac
  if httpBody and len(httpBody) > 0:
    md5 = hashlib.md5()
    md5.update(json.dumps(httpBody).encode('utf-8')) # we add it as a json string
    hm.update(md5.hexdigest().encode('utf-8'))

  return hm.hexdigest() # returns hex

def parse_response(re):
    if re.get('Hits').get('Blacklist') == 0:
        return {'data':re.get('Result'),'channel':'hadu'}
    else:
        return RETRY_LATER


def vrify_black_from_hadu(nik,mobile_no,name):
    times = str(int(time.time()))
    jsondata = {"nik":str(int(nik)),"mobile_no":str(mobile_no)[3:],"name":str(name)}
    print(jsondata)
    HexSignature = signRequest('sha256',keySecret,times,'POST','/api/v1/query/identity',jsondata)
    auth = 'HMAC sha256 {} {} {}'.format(times,keyid,HexSignature)
    re = requests.post('https://api.vguard.ai/api/v1/query/identity',json=jsondata,headers={'Authorization':auth})
    re.close()
    return re.json()

def bank_holder_vrify_from_hadu(bank_code,account_no,holder_name):
    times = str(int(time.time()))
    jsondata = {"bank_code":str(bank_code),"account_no":str(account_no),"holder_name":str(holder_name)}
    print(jsondata)
    HexSignature = signRequest('sha256',keySecret,times,'POST','/api/v3/holder_verify',jsondata)
    auth = 'HMAC sha256 {} {} {}'.format(times,keyid,HexSignature)
    re = requests.post('https://api.vguard.ai/api/v3/holder_verify',json=jsondata,headers={'Authorization':auth})
    re.close()
    return re.json()



if __name__ == '__main__':
    print(bank_holder_vrify_from_hadu('BCA','6044061044','YUSTINA YANGGA'))



