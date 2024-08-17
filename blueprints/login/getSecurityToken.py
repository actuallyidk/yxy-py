import requests
from flask import jsonify, request

from utils import getBaseResponse, getErrorResponse
from yxyClient import yxyClient
from consts import COMPUS_URL


def getSecurityToken():
    params = request.args or request.json
    yxy = yxyClient(**params)
    req_data = yxy.getBaseRequest()
    req_data['sceneCode'] = 'app_user_login'
    res = requests.post(
        COMPUS_URL + "/common/security/token",
            json=req_data,
            headers={"User-Agent": yxy.ua}
    ).json()
    
    try:
        return getBaseResponse({
            "level": res.get("data").get("level"),
            "token": res.get("data").get("securityToken")
        })
    except:
        return getErrorResponse(res)