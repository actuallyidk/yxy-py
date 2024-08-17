from flask import Blueprint

from .getCardBalance import getCardBalance
from .getConsumptionRecord import getConsumptionRecord


bp_user = Blueprint("bp_user", __name__)

bp_user.route('/card_balance', methods=['GET'])(getCardBalance)
bp_user.route('/consumption_record', methods=['GET'])(getConsumptionRecord)