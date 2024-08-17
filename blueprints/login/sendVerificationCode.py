import base64
import time

from flask import request
from Crypto.Hash import MD5
from Crypto.Cipher import AES
import requests


from consts import APP_ALL_VERSION, COMPUS_URL
from utils import getBaseResponse, getErrorResponse
from yxyClient import yxyClient


def sendVerificationCode():
    params = request.args or request.json
    yxy = yxyClient(**params)

    req_data = yxy.getBaseRequest()
    req_data['mobilePhone'] = params.get("phone_num")
    req_data['securityToken'] = params.get("security_token")
    req_data['appSecurityToken'] = getAppSecurityToken(params)
    req_data['sendCount'] = 1
    captcha = params.get("captcha")
    if captcha:
        req_data['imageCaptchaValue'] = captcha

    res = requests.post(
        COMPUS_URL + "/compus/user/sendLoginVerificationCode",
        json=req_data,
        headers={"User-Agent": yxy.ua}
    ).json()

    try:
        return getBaseResponse({
            'user_exists': res.get("data").get("userExists")
        })
    except:
        return getErrorResponse(res)


def getAppSecurityToken(params: dict) -> str:
    securityToken = params.get("security_token")
    device_id = params.get("device_id")

    def pkcs5_padding(s): return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    key = securityToken[0: 16]
    token = securityToken[32:]
    cipher = AES.new(key.encode(), mode=AES.MODE_ECB)
    t = cipher.decrypt(base64.b64decode(token)).decode()
    # unpadding
    t = t[:-ord(t[-1])]
    ts = str(time.time())
    s = MD5.new(
        MD5.new(
            (device_id + '|YUNMA_APP|' + t + '|' +
             ts + '|' + APP_ALL_VERSION).encode()
        ).hexdigest().upper().encode()
    ).hexdigest().upper()

    appSecurityToken = base64.b64encode(cipher.encrypt(
        pkcs5_padding(device_id + '|YUNMA_APP|' + t + '|' +
                      ts + '|' + APP_ALL_VERSION + '|' + s).encode()
    )
    ).decode()

    return appSecurityToken