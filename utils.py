import uuid
from Crypto.Hash import MD5

def gen_random_fake_md5():
    return MD5.new(uuid.uuid4().bytes).hexdigest()

def getBaseResponse(data):
    return {
        "code": 0,
        "msg": "success",
        "data": data
    }

def getErrorResponse(res):
    return {
        "code": res.get("statusCode"),
        "msg": res.get("message"),
        "data": res.get("data")
    }