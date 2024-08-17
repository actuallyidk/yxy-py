from flask import request
import requests
from consts import APP_ALL_VERSION, CLIENT_ID, COMPUS_URL
from utils import gen_random_fake_md5, getBaseResponse, getErrorResponse
from yxyClient import yxyClient


def loginBySilent():
    params = request.args or request.json
    yxy = yxyClient(**params)

    req_data = yxy.getBaseRequest()
    req_data['appAllVersion'] = APP_ALL_VERSION
    req_data["appPlatform"] = "Android"
    req_data["brand"] = "Android"
    req_data["clientId"] = CLIENT_ID
    req_data["mobilePhone"] = params.get("phone_num")
    req_data["mobileType"] = "Android for arm64"
    req_data["osType"] = "Android"
    req_data["osVersion"] = "12"
    req_data["token"] = params.get("token") or gen_random_fake_md5()
    req_data["ymId"] = params.get("uid")

    print(req_data)

    res = requests.post(
        COMPUS_URL + "/login/doLoginBySilent",
        json=req_data,
        headers={"User-Agent": yxy.ua}
    ).json()

    try:
        return getBaseResponse({
            "uid": res.get("data").get("id"),
            "token": res.get("data").get("token"),
            "device_id": res.get("data").get("deviceId"),
            "bind_card_status": res.get("data").get("bindCardStatus")
        })
    except:
        return getErrorResponse(res)