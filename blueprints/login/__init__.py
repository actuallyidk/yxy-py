from flask import Blueprint

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