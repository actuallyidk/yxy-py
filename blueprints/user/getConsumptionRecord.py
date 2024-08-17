from flask import request
import requests
from consts import COMPUS_URL, SCHOOL_CODE
from utils import gen_random_fake_md5, getBaseResponse, getErrorResponse
from yxyClient import yxyClient


def getConsumptionRecord():
    params = request.args or request.json

    yxy = yxyClient(**params)

    req_data = yxy.getBaseRequest()
    req_data['ymId'] = params.get("uid")
    req_data['schoolCode'] = SCHOOL_CODE
    req_data['token'] = params.get("token") or gen_random_fake_md5()
    req_data['queryTime'] = params.get("query_time")
    

    res = requests.post(
        COMPUS_URL + "/routeauth/auth/route/user/cardQuerynoPage",
        json=req_data,
        headers={"User-Agent": yxy.ua}
    ).json()

    try:
        return getBaseResponse([{
            "address": i.get("address"),
            "money": i.get("money"),
            "time": i.get("time")
        } for i in res.get('rows')])
    except:
        return getErrorResponse(res)