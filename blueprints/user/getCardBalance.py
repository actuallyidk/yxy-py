from flask import request
import requests

from consts import COMPUS_URL, SCHOOL_CODE
from utils import gen_random_fake_md5, getBaseResponse, getErrorResponse
from yxyClient import yxyClient


def getCardBalance():
    params = request.args or request.json

    yxy = yxyClient(**params)

    req_data = yxy.getBaseRequest()
    req_data['schoolCode'] = SCHOOL_CODE
    req_data['token'] = params.get("token") or gen_random_fake_md5()
    req_data['walletNo'] = "1"
    req_data['ymId'] = params.get("uid")

    res = requests.post(
        COMPUS_URL + "/compus/user/getCardMoney",
        json=req_data,
        headers={"User-Agent": yxy.ua}
    ).json()

    try:
        return getBaseResponse({
            "balance": res.get("data")
        })
    except:
        return getErrorResponse(res)