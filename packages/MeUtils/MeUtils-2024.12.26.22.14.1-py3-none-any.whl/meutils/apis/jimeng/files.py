#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : kaiyuan
# @Time         : 2024/12/18 16:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

import hmac
import zlib
import hashlib

from meutils.pipe import *
from meutils.caches.redis_cache import cache


def random_str(n):
    return ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba0123456789', n))


def hash256(msg):
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()


def hmac_hash256(key, msg):
    if type(key) == str:
        return hmac.new(key.encode('utf-8'), msg.encode('utf-8'), hashlib.sha256)
    elif type(key) == hmac.HMAC:
        return hmac.new(key.digest(), msg.encode('utf-8'), hashlib.sha256)


def fileCRC32(file_buffer):
    return hex(zlib.crc32(file_buffer) & 0xFFFFFFFF)[2:]


def u(params):
    new_params = sorted(params.items(), key=lambda x: x[0])
    new_params = [f"{k}={v}" for k, v in new_params]
    return "&".join(new_params)


class JJRequest:
    def __init__(self, e, t, api, method="GET", params=None, data=None):
        self.t = t
        self.e = e
        self.api = api
        self.method = method
        self.params = params
        self.data = data

    def getAuthorization(self):
        return f"AWS4-HMAC-SHA256 Credential={self.e['access_key_id']}/{self.t[0:8]}/cn-north-1/imagex/aws4_request, SignedHeaders=x-amz-date;x-amz-security-token, Signature={self.signature()}"

    def signature(self):
        r = self.getSigningKey()
        return hmac_hash256(r, self.stringToSign()).hexdigest()

    def getSigningKey(self, r="cn-north-1", n="imagex"):
        o = hmac_hash256("AWS4" + self.e['secret_access_key'], str(self.t[0:8]))
        i = hmac_hash256(o, str(r))
        s = hmac_hash256(i, str(n))
        return hmac_hash256(s, "aws4_request")

    def stringToSign(self):
        t = []
        t.append("AWS4-HMAC-SHA256")
        t.append(self.t)
        t.append(self.credentialString())
        t.append(hash256(self.canonicalString()))
        return "\n".join(t)

    def credentialString(self, region="cn-north-1", serviceName="imagex"):
        return "/".join([self.t[0:8], region, serviceName, "aws4_request"])

    def canonicalString(self):
        e = []
        e.append(self.method)
        e.append("/")
        e.append(u(self.params))
        e.append(self.canonicalHeaders())
        e.append(self.signedHeaders())
        e.append(self.hexEncodedBodyHash())
        return "\n".join(e)

    def canonicalHeaders(self):
        return f"x-amz-date:{self.t}\nx-amz-security-token:{self.e['session_token']}\n"

    def signedHeaders(self):
        return "x-amz-date;x-amz-security-token"

    def hexEncodedBodyHash(self):
        return hash256("")


@cache(ttl=15 * 60)
def upload(image: bytes, upload_token: dict):  # oss 跨账号不知道是否可以使用
    # e = auth = upload_token['data']['auth'] # 豆包
    data = upload_token['data']
    service_id = data.get('service_id', '3jr8j4ixpe')  # 即梦 3jr8j4ixpe 豆包 a9rns2rl98

    if 'auth' in data:
        data = data['auth']

    session_token = data['session_token']

    t = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

    params = {
        "Action": "ApplyImageUpload",
        "Version": "2018-08-01",
        "ServiceId": service_id,
        "s": random_str(10),

        "FileExtension": ".png",  #####
        "FileSize": len(image),
    }

    r = JJRequest(data, t, "https://imagex.bytedanceapi.com/", method="GET", params=params)
    headers = {
        'authorization': r.getAuthorization(),
        'x-amz-date': t,
        'x-amz-security-token': session_token,
    }
    # logger.debug(headers)
    response = requests.get(r.api, params=params, headers=headers)
    response.raise_for_status()
    logger.debug(response.status_code)
    response = response.json()

    logger.debug(bjson(response))
    if "Result" not in response:
        return

    store_info = response['Result']['UploadAddress']['StoreInfos'][0]
    logger.debug(bjson(store_info))

    oss_uri = store_info['StoreUri']
    oss_token = store_info['Auth']

    headers = {
        "authorization": oss_token,
        "content-length": str(len(image)),
        "content-Type": "image/jpeg",
        "content-crc32": fileCRC32(image),
    }

    # oss_url = f"https://{resp['Result']['UploadAddress']['UploadHosts'][0]}/{oss_uri}"

    # image_resp = requests.put(  # post
    #     oss_url,
    #     headers=headers,
    #     data=image,
    # )
    # logger.debug(image_resp.json())

    # return get_url(StoreUri)

    # upload_url = f"https://tos-hl-x.snssdk.com/upload/v1/{oss_uri}"
    upload_url = f"https://{response['Result']['UploadAddress']['UploadHosts'][0]}/upload/v1/{oss_uri}"

    response = requests.post(upload_url, headers=headers, data=image)
    response.raise_for_status()
    response = response.json()

    logger.debug(response)

    return oss_uri


if __name__ == "__main__":
    from meutils.apis.jimeng.common import get_upload_token

    # 豆包
    token = "de2215a7bb8e442774cf388f03fac84c"

    # jimeng
    token = "693701c43e477b7c405cc7e2fef0ddbd"
    #
    upload_token = arun(get_upload_token(token))

    #
    # with open("11.jpg", "rb") as f:
    #     file = image = f.read()
    #
    #     upload(image, upload_token)
