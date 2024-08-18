from flask import request
import requests
from consts import APPLICATION_URL, AUTH_URL, SCHOOL_CODE
from utils import getBaseResponse, getErrorResponse
from yxyClient import yxyClient


def getAuth():
    params = request.args or request.json

    yxy = yxyClient(**params)

    req_data = {
        "bindSkip": "1",    # Magic Number
        "authType": "2",    # Magic Number
        "ymAppId": "1810181825222034",  # Magic Number
        "callbackUrl": APPLICATION_URL + "/",
        "unionid": params.get("uid"),
        "schoolCode": SCHOOL_CODE,
    }

    res = requests.get(
        AUTH_URL + "/authoriz/getCodeV2",
        params=req_data,
        headers={"User-Agent": yxy.ua},
        allow_redirects=False
    )

    # https://application.xiaofubao.com/?errCode=0&ymCode=d2b7de1c72cb48c4b2fa63b448ca6f04
    location = res.headers.get("Location")
    if not location:
        raise Exception("未获取到 OAuth Code")

    ymCode = location.split("ymCode=")[1].split("&")[0]

    res = requests.post(
        APPLICATION_URL + "/app/login/getUser4Authorize",
        data={
            "code": ymCode,
        },
        headers={"User-Agent": yxy.ua}
    )

    try:
        return getBaseResponse({
            "token": res.headers.get('Set-Cookie').split('shiroJID=')[1].split(';')[0]
        })
    except:
        return getErrorResponse(res)
