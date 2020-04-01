#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Date    :   18/04/26 16:47:20
#   Desc    :   
#
import hmac
import json
import time
import hashlib
import datetime
import base64
import time
import sys
import requests
requests.packages.urllib3.disable_warnings()

if sys.version_info.major == 2:
    from urllib import urlencode
    from urllib import quote
    from urlparse import urlparse
else:
    from urllib.parse import urlencode
    from urllib.parse import quote
    from urllib.parse import urlparse

class BaseClient(object):

    def __init__(self, ak, sk):
        self._ak = ak
        self._sk = sk
        self.__client = requests
        self.__connectTimeout = 60.0
        self.__socketTimeout = 60.0
        self._proxies = {}

    def request(self, url, data):
        params = {}
        headers = {}
        headers = self._getAuthHeaders('POST', url, params, headers)
        response = self.__client.post(url, data=data, params=params, 
            headers=headers, verify=False,
            timeout=(self.__connectTimeout, self.__socketTimeout,),
            proxies=self._proxies)
        response.close()
        #return response.json()
        return response.json()

    def _getAuthHeaders(self, method, url, params=None, headers=None):
        """
            api request http headers
        """

        headers = headers or {}
        params = params or {}

        urlResult = urlparse(url)
        for kv in urlResult.query.strip().split('&'):
            if kv:
                k, v = kv.split('=')
                params[k] = v

        # UTC timestamp
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

        #headers['Host'] = urlResult.hostname
        headers['credit-date'] = timestamp
        version, expire = '1', '1800'

        # 1 Generate SigningKey
        val = "credit-v%s/%s/%s/%s" % (version, self._ak, timestamp, expire)
        signingKey = hmac.new(self._sk.encode('utf-8'), val.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # 2 Generate CanonicalRequest
        # 2.1 Genrate CanonicalURI
        canonicalUri = quote(urlResult.path)
        # 2.2 Generate CanonicalURI: not used here
        # 2.3 Generate CanonicalHeaders: only include host here
        
        canonicalHeaders = []
        for header, val in headers.items():
            canonicalHeaders.append(
                '%s:%s' % (
                    quote(header.strip(), '').lower(), 
                    quote(val.strip(), '')
                )
            )
        canonicalHeaders = '\n'.join(sorted(canonicalHeaders))

        # 2.4 Generate CanonicalRequest
        canonicalRequest = '%s\n%s\n%s\n%s' % (
            method.upper(),
            canonicalUri,
            '&'.join(sorted(urlencode(params).split('&'))),
            canonicalHeaders
        )
        # 3 Generate Final Signature 
        signature = hmac.new(signingKey.encode('utf-8'), canonicalRequest.encode('utf-8'),
                        hashlib.sha256
                    ).hexdigest()

        headers['authorization'] = 'credit-v%s/%s/%s/%s/%s/%s' % (
            version,
            self._ak,
            timestamp,
            expire, 
            ';'.join(headers.keys()).lower(),
            signature
        )

        return headers





