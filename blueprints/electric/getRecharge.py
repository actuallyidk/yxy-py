from flask import request
import requests
from consts import APPLICATION_URL
from utils import getBaseResponse, getErrorResponse
from yxyClient import yxyClient


def getRecharge():
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
        req_data['subType'] = "100304"
        req_data['currentPage'] = params.get("page")
        res = requests.post(
            APPLICATION_URL + "/app/electric/queryISIMSRoomBuyRecord",
            data=req_data,
            headers={
                "User-Agent": yxy.ua,
                "Cookie": "shiroJID=" + params.get("token")
            }
        ).json()

        print(res)

        try:
            return getBaseResponse([
                {
                    "datetime": i.get("datetime"),
                    "money": i.get("money")
                } for i in res.get("rows")
            ])
        except:
            return getErrorResponse(res)
    elif campus == "mgs":
        req_data['pageNo'] = params.get("page")
        req_data['pageSize'] = 30

        res = requests.post(
            APPLICATION_URL + "/app/electric/roomBuyRecord",
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
                    "money": i.get("amount")
                } for i in res.get("rows")
            ])
        except:
            return getErrorResponse(res)
