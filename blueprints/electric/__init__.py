from flask import Blueprint, request

from .getAuth import getAuth
from .getAmount import getAmount
from .getRecharge import getRecharge
from .getConsumption import getConsumption

bp_electric = Blueprint("bp_electric", __name__)

bp_electric.route('/auth', methods=['GET'])(getAuth)
bp_electric.route('/amount', methods=['GET'])(getAmount)
bp_electric.route('/recharge', methods=['GET'])(getRecharge)
bp_electric.route('/consumption', methods=['GET'])(getConsumption)

required_params = {
    "/auth": ['uid'],
    "/amount": ['token', 'campus'],
    "/recharge": ['token', 'campus', 'room_str_concat'],
    "/consumption": ['token', 'campus', 'room_str_concat']
}

@bp_electric.before_request
def check_params():
    if request.path in required_params:
        for param in required_params[request.path]:
            if param not in request.args:
                return {
                    'code': 1,
                    'msg': '参数错误'
                }, 400