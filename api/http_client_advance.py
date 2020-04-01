#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
import os
import requests
import time
import sys
from datetime import datetime
from random import randint


class OpenApiClient(object):
    """ADVANCE.AI's open api client."""

    api_host = None
    access_key = None
    secret_key = None
    time_out = 60

    request_url = None
    request_headers = None
    request_post_body = None

    def __init__(self, api_host=None, access_key=None, secret_key=None):
        self.api_host = api_host
        self.access_key = access_key
        self.secret_key = secret_key

    def _hmac_base64(self, sign_str=''):
        PY2 = sys.version_info[0] == 2
        secret = bytes(sign_str).encode('utf-8') if PY2 else bytes(sign_str, 'utf-8')
        message = bytes(self.secret_key).encode('utf-8') if PY2 else bytes(self.secret_key, 'utf-8')
        signature = base64.b64encode(hmac.new(message, secret, digestmod=hashlib.sha256).digest())
        if PY2:
            return signature
        else:
            return signature.decode('utf-8')

    def _is_scalar(self, value):
        return isinstance(value, (type(None), str, int, float, bool, unicode))

    def set_timeout(self, timeout):
        self.time_out = timeout

    def _prepare(self, api_name, param_dict, file_dict):
        if not api_name.startswith('/'):
            api_name = '/' + api_name

        self.request_url = self.api_host[:-1] if self.api_host.endswith('/') else self.api_host
        self.request_url += api_name

        if not file_dict:
            content_type = 'application/json'
            self.request_post_body = json.dumps(param_dict)
        else:
            self.request_post_body = ''
            rand_int = 10000000 + randint(0, 10000000 - 1)
            boundary = '----AD1238MJL7' + str(int(round(time.time() * 1000))) + 'I' + str(rand_int)
            content_type = 'multipart/form-data; boundary={}'.format(boundary)

            if param_dict:
                for k, v in param_dict.items():
                    if not self._is_scalar(v):
                        raise RuntimeError("only scalar key/value params support when uploading files")
                    self.request_post_body += "--{}\r\n".format(boundary)
                    self.request_post_body += 'Content-Disposition: form-data; name="{}"\r\n'.format(k)
                    self.request_post_body += "\r\n{}\r\n".format(v)

            for k, fn in file_dict.items():
                if not os.path.exists(fn):
                    raise RuntimeError("{} not exists".format(fn))
                base_name = os.path.basename(fn)
                file_type = base_name.split('.')[1]
                if file_type == 'jpg':
                    file_type = 'jpeg'
                if file_type != 'jpeg' and file_type != 'png':
                    raise RuntimeError("{} file type not support, only support jpeg/jpg/png.".format(file_type))
                mime_type = 'image/' + file_type
                with open(fn, 'rb') as fd:
                    file_content = fd.read(10000000)  # Max image size 10M
                self.request_post_body += "--{}\r\n".format(boundary)
                self.request_post_body += 'Content-Disposition: form-data; name="{}"; filename="{}"\r\n'.format(k,
                                                                                                                base_name)
                self.request_post_body += "Content-Type: {}\r\n".format(mime_type)
                self.request_post_body += "\r\n{}\r\n".format(file_content)

            self.request_post_body += "--{}--".format(boundary)

        now = datetime.utcnow()
        gmt_now = now.strftime("%a, %d %b %Y %H:%M:%S") + ' GMT'

        separator = '$'
        sign_str = 'POST' + separator
        sign_str += api_name + separator
        sign_str += gmt_now + separator
        authorization = '{}:{}'.format(self.access_key, self._hmac_base64(sign_str=sign_str))

        self.request_headers = {
            'Content-Type': content_type,
            'Date': gmt_now,
            'Authorization': authorization
        }

    def request(self, api_name, param_array=None, file_array=None):
        self._prepare(api_name, param_array, file_array)

        resp = requests.request(
            url=self.request_url,
            method='POST',
            headers=self.request_headers,
            data=self.request_post_body,
            timeout=self.time_out
        )
        resp.close()
        return resp.json()
