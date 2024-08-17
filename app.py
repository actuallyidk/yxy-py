from flask import Flask

from blueprints.login import bp_login
from blueprints.user import bp_user
from blueprints.electric import bp_electric

app = Flask(__name__)

app.register_blueprint(bp_login, url_prefix="/v2/login")
app.register_blueprint(bp_user, url_prefix="/v2/user")
app.register_blueprint(bp_electric, url_prefix="/v2/electric")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)