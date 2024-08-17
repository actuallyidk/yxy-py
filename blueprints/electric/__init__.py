from flask import Blueprint

from .getAuth import getAuth
from .getBind import getBind
from .getAmount import getAmount
from .getRecharge import getRecharge
from .getConsumption import getConsumption

bp_electric = Blueprint("bp_electric", __name__)

bp_electric.route('/auth', methods=['GET'])(getAuth)
bp_electric.route('/bind', methods=['GET'])(getBind)
bp_electric.route('/amount', methods=['GET'])(getAmount)
bp_electric.route('/recharge', methods=['GET'])(getRecharge)
bp_electric.route('/consumption', methods=['GET'])(getConsumption)