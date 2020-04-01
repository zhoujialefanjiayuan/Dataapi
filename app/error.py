"""
错误返回
{
  "status": 401,
  "message": "出错信息"
}

正确返回
{
  "status": 200,
  "data":{}
}
"""

#余额不足
INSUFFICIENT_BALANCE = {
  "status": 401,
  "message": "insufficient balance"
}


#请求参数不合法
INVALID_PARAMETER_ERROR = {
  "status": 401,
  "message": "invalid parameter error"
}


#验证不通过，用户不存在或者校验信息有误
NO_AUTHORIZATION = {
  "status": 401,
  "message": "no authorization"
}

#auth拼接错误  {ACCESS_KEY} {timestamp} {sign}
Authorization_format_error = {
    "status": 401,
    "message": "authorization format error"
}

#系统错误
RETRY_LATER = {
  "status": 401,
  "message": "retry later"
}



