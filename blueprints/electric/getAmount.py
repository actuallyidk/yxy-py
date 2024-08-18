from flask import jsonify, request
import requests

from consts import APPLICATION_URL
from utils import getBaseResponse, getErrorResponse
from yxyClient import yxyClient


def getAmount():
    params = request.args or request.json

    yxy = yxyClient(**params)

    campus = params.get("campus")

    if campus == "zhpf":
        bindType = "3"
    elif campus == "mgs":
        bindType = "1"
    else:
        return jsonify({
            "code": 1,
            "msg": "参数错误",
            "data": {}
        }), 400

    req_data = {
        "bindType": bindType,
        "platform": "YUNMA_APP",
    }

    res = requests.post(
        APPLICATION_URL + "/app/electric/queryBind",
        json=req_data,
        headers={
            "User-Agent": yxy.ua,
            "Cookie": "shiroJID=" + params.get("token")
        }
    ).json()

    areaId = res.get("rows")[0].get("areaId")
    buildingCode = res.get("rows")[0].get("buildingCode")
    floorCode = res.get("rows")[0].get("floorCode")
    roomCode = res.get("rows")[0].get("roomCode")

    room_str_concat = areaId + '#' + buildingCode + '#' + floorCode + '#' + roomCode

    req_data = {
        "areaId": areaId,
        "buildingCode": buildingCode,
        "floorCode": floorCode,
        "roomCode": roomCode,
        "platform": "YUNMA_APP"
    }

    if campus == "zhpf":
        res = requests.post(
            APPLICATION_URL + "/app/electric/queryISIMSRoomSurplus",
            data=req_data,
            headers={
                "User-Agent": yxy.ua,
                "Cookie": "shiroJID=" + params.get("token")
            }
        ).json()

        print(res)

        try:
            return getBaseResponse({
                "surplus": res.get("data").get("surplusList")[0].get("surplus"),
                "amount": res.get("data").get("surplusList")[0].get("amount"),
                "room_str_concat": room_str_concat + "#" + res.get("data").get("surplusList")[0].get("mdtype"),
                "display_room_name": res.get("data").get("displayRoomName")
            })
        except:
            return getErrorResponse(res)
        
    elif campus == "mgs":
        res = requests.post(
            APPLICATION_URL + "/app/electric/queryRoomSurplus",
            data=req_data,
            headers={
                "User-Agent": yxy.ua,
                "Cookie": "shiroJID=" + params.get("token")
            }
        ).json()

        try:
            return getBaseResponse({
                "surplus": res.get("data").get("surplus"),
                "amount": res.get("data").get("amount"),
                "display_room_name": res.get("data").get("displayRoomName"),
                "room_str_concat": room_str_concat
            })
        except:
            return getErrorResponse(res)
        



