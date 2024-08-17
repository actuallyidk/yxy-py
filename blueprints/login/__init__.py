from flask import Blueprint, request

from .getSecurityToken import getSecurityToken
from .getCaptchaImage import getCaptchaImage
from .sendVerificationCode import sendVerificationCode
from .loginByCode import loginByCode
from .loginBySilent import loginBySilent

bp_login = Blueprint("bp_login", __name__)

bp_login.route('/security_token', methods=['GET'])(getSecurityToken)
bp_login.route('/captcha_image', methods=['GET'])(getCaptchaImage)
bp_login.route('/send_verification_code', methods=['POST'])(sendVerificationCode)
bp_login.route('/by_code', methods=['POST'])(loginByCode)
bp_login.route('/silent', methods=['POST'])(loginBySilent)

required_params = {
    '/security_token': ['device_id'],
    '/captcha_image': ['device_id', 'security_token'],
    '/send_verification_code': ['device_id', 'security_token', 'phone_num'],
    '/by_code': ['device_id', 'phone_num', 'code'],
    '/silent': ['device_id', 'uid'],
}

@bp_login.before_request
def check_params():
    if request.path in required_params:
        for param in required_params[request.path]:
            if param not in request.args:
                return {
                    'code': 1,
                    'msg': '参数错误'
                }, 400