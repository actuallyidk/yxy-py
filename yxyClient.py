import uuid
from consts import (
    APP_ALL_VERSION,
    APP_VERSION
)

class yxyClient:
    def __init__(self, **kwargs):
        self.phone_num = kwargs.get("phone_num")
        self.yxy_uid = kwargs.get("yxy_uid")
        self.device_id = kwargs.get("device_id") or str(uuid.uuid4()).replace("-", "")
        if not self.device_id.startswith("ym-"):
            self.device_id = "ym-" + self.device_id
        self.ua = (
            "Mozilla/5.0 (Linux; Android 12; Android for arm64; wv) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Version/4.0 Chrome/126.0.6478.186 Mobile Safari/537.36 "
            "ZJYXYwebviewbroswer ZJYXYAndroid tourCustomer/yunmaapp.NET/"
            f"{APP_ALL_VERSION}/"
            f"{self.device_id}"
        )

    def getBaseRequest(self):
        return {
            "appVersion": APP_VERSION,
            "deviceId": self.device_id,
            "platform": "YUNMA_APP",
            "schoolCode": "",
            "testAccount": 1,
            "token": ""
        }
