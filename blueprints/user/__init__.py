from flask import Blueprint, request

from .getCardBalance import getCardBalance
from .getConsumptionRecord import getConsumptionRecord


bp_user = Blueprint("bp_user", __name__)

bp_user.route('/card_balance', methods=['GET'])(getCardBalance)
bp_user.route('/consumption_records', methods=['GET'])(getConsumptionRecord)

required_params = {
    '/card_balance': ['device_id', 'uid'],
    '/consumption_record': ['device_id', 'uid', 'query_time']
}

@bp_user.before_request
def check_params():
    if request.path in required_params:
        for param in required_params[request.path]:
            if param not in request.args:
                return {
                    'code': 1,
                    'msg': '参数错误'
                }, 400