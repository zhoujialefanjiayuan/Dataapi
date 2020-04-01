import hmac
import json

from flask import request, jsonify

from app.error import Authorization_format_error, NO_AUTHORIZATION, INSUFFICIENT_BALANCE

# ACCESS_KEY = ''  #公钥 ，锁定用户身份
# SECRET_KEY= ''  #私钥，用于加密
from app.ext import db
from app.models import User, Api_log, NikMultiPlatform, MobileMultiPlatform


#auth拼接  {ACCESS_KEY} {timestamp} {sign}
def signRequest(secret, timestamp, httpMethod, originalUrl):
  '''
  Sign HTTP Request
  :param str  secret      : your secret
  :param str  timestamp   : current unix timestamp (second)
  :param str  httpMethod  : upper case http method like GET
  :param str  originalUrl : original url without host like /api/path?params
  :return: hex signature
  :rtype: str
  '''
  hm = hmac.new(secret.encode('utf-8')) #
  hm.update(timestamp.encode('utf-8')) # add timestamp provided in header to make sure it hasn't been changed
  hm.update(httpMethod.encode('utf-8')) # add verb e.g POST, GET
  hm.update(originalUrl.encode('utf-8')) # add url e.g /api/order?id=1

  return hm.hexdigest() # returns hex

def load_middleware(app):
    @app.before_request
    def before_request():
        auth = request.headers['Authorization'].split(' ')
        if len(auth) != 3:
            return jsonify(Authorization_format_error)
        path = request.path
        method = request.method
        theuser = User.query.get(auth[0])
        secret_key = theuser.secretkey
        server_auth = signRequest(secret_key,auth[1],method,path)
        #校验签名
        if server_auth == auth[2]:
            #查询余额
            balance = theuser.balance
            extend_balance = theuser.extend_balance
            if balance + extend_balance <= 0:
                return INSUFFICIENT_BALANCE
            request.data = theuser.username
        else:
            return NO_AUTHORIZATION

    @app.after_request
    def after_request(response):
        senddata = json.loads(response.data)
        if 'status' not in senddata:
            response.data = json.dumps({'status':200,'data':senddata})
        #存储用户调用日志
        findauth = request.headers['Authorization'].split(' ')
        params = request.json
        logmodel = Api_log.model(request.data,findauth[0])
        logmodel.apiname = request.path.split('/')[-1]
        logmodel.params = json.dumps(params)
        logmodel.nik = params.get('nik','')
        logmodel.mobile_no = params.get('mobile_no','')
        logmodel.response_code = senddata.get('status',200)
        logmodel.paied = senddata.get('paied')
        logmodel.applytime = findauth[1]
        logmodel.add_db_data()
        # 存储身份证多头
        if params.get('nik'):
            nikmul = NikMultiPlatform()
            nikmul.nik = params.get('nik')
            nikmul.user = findauth[0]
            nikmul.channel = 'inner'
            nikmul.add_db_data()
        if params.get('mobile_no'):
            mobilemul = MobileMultiPlatform()
            mobilemul.mobile_no = params.get('mobile_no')
            mobilemul.user = findauth[0]
            mobilemul.channel = 'inner'
            mobilemul.add_db_data()
        return response