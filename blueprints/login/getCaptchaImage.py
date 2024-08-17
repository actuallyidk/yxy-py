from flask import request
import requests

from consts import COMPUS_URL
from utils import getBaseResponse, getErrorResponse
from yxyClient import yxyClient


def getCaptchaImage():
    params = request.args or request.json
    yxy = yxyClient(**params)
    req_data = yxy.getBaseRequest()
    req_data['securityToken'] = params.get("security_token")

    res = requests.post(
        COMPUS_URL + "/common/security/imageCaptcha",
        json=req_data,
        headers={"User-Agent": yxy.ua}
    ).json()

    try:
        return getBaseResponse({
            "img": res.get("data")
        })
    except:
        return getErrorResponse(res)
