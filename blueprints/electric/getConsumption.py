from flask import jsonify, request
import requests
from consts import APPLICATION_URL
from utils import getBaseResponse, getErrorResponse
from yxyClient import yxyClient


def getConsumption():
    params = request.args or request.json

    yxy = yxyClient(**params)

    campus = params.get("campus")
    room_str_concat = params.get("room_str_concat")

    req_data = {
        "areaId": room_str_concat.split('#')[0],
        "buildingCode": room_str_concat.split('#')[1],
        "floorCode": room_str_concat.split('#')[2],
        "roomCode": room_str_concat.split('#')[3],
        "platform": "YUNMA_APP"
    }

    if campus == "zhpf":
        req_data['mdtype'] = room_str_concat.split('#')[4]
        res = requests.post(
            APPLICATION_URL + "/app/electric/getISIMSRecords",
            data=req_data,
            headers={
                "User-Agent": yxy.ua,
                "Cookie": "shiroJID=" + params.get("token")
            }
        ).json()

        try:
            return getBaseResponse([
                {
                    "datetime": i.get("datetime"),
                    "use": i.get("used")
                } for i in res.get("rows")
            ])
        except:
            return getErrorResponse(res)
    elif campus == "mgs":
        req_data['pageNo'] = 1,
        req_data['pageSize'] = 30

        res = requests.post(
            APPLICATION_URL + "/app/electric/queryUsageRecord",
            data=req_data,
            headers={
                "User-Agent": yxy.ua,
                "Cookie": "shiroJID=" + params.get("token")
            }
        ).json()

        try:
            return getBaseResponse([
                {
                    "datetime": i.get("dateTime"),
                    "use": i.get("dayUsage")
                } for i in res.get("rows")
            ])
        except:
            return getErrorResponse(res)
    else:
        return jsonify({
            "code": 1,
            "msg": "参数错误",
            "data": {}
        }), 400