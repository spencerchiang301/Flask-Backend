from datetime import timedelta
from flask_jwt_extended import get_jwt_identity, get_jwt, JWTManager
from flask_jwt_extended import jwt_required
from flask import Flask, request
from flask_cors import CORS
import configparser, json

from Routing.JWT.views import jwt_blueprints
from Routing.PostNote.views import postNote_blueprints
from Routing.Navigation.views import navigation_blueprints
from Routing.Contact.views import contact_blueprints
from Routing.Calendar.views import calendar_blueprints
from Routing.Summary.views import summary_blueprints
from Routing.Setting.views import setting_blueprints
from Module.Auth.MyUser import MyUser
from Routing.Setting.MySetting import MySetting

config = configparser.ConfigParser()
config.read('Setting/config.ini')

secret = config['app']['secret']
jwtSecret = config['jwt']['secret']

app = Flask(__name__)
app.register_blueprint(jwt_blueprints, url_prefix='/jwt')
app.register_blueprint(postNote_blueprints, url_prefix='/postNote')
app.register_blueprint(navigation_blueprints, url_prefix='/navigation')
app.register_blueprint(calendar_blueprints, url_prefix='/calendar')
app.register_blueprint(contact_blueprints, url_prefix='/contact')
app.register_blueprint(summary_blueprints, url_prefix='/summary')
app.register_blueprint(setting_blueprints, url_prefix='/setting')
CORS(app, resources={r"/*": {"origins": ["*"]}})
app.secret_key = bytes(secret, 'UTF-8')
ACCESS_EXPIRES = timedelta(hours=1)
app.config["JWT_SECRET_KEY"] = jwtSecret
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager()
jwt.init_app(app)

@app.route("/getLogin", methods=['POST'])
def getLogin():
    json_data = json.loads(request.get_data().decode('utf8').replace("'", '"'))
    email = json_data['email']
    password = json_data['password']
    db = MyUser()
    db.loginUser(email, password)
    finalDict = db.getResult()
    return finalDict


@app.route("/updatePassword", methods=['POST'])
@jwt_required()
def updatePassword():
    words = request.get_json()['words']
    oldPassword = request.get_json()['oldPassword']
    newPassword = request.get_json()['newPassword']
    if words == get_jwt_identity():
        db = MyUser()
        db.updatePassword(words, oldPassword, newPassword)
        return db.getResult()
    else:
        return "Token is inValid"


@app.route("/updateRescueInfo", methods=['POST'])
@jwt_required()
def updateRescueInfo():
    words = request.get_json()['words']
    phone = request.get_json()['phone']
    contact1 = request.get_json()['contact1']
    contact2 = request.get_json()['contact2']
    if words == get_jwt_identity():
        db = MyUser()
        db.updateRescueInfo(words, phone, contact1, contact2)
        return db.getResult()
    else:
        return "Token is inValid"


@app.route("/getLogout", methods=["DELETE"])
@jwt_required(verify_type=False)
def getLogout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    # jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    return f"{ttype.capitalize()} token successfully revoked"

@app.route("/getRegister", methods=['POST'])
def getRegister():
    json_data = json.loads(request.get_data().decode('utf8').replace("'", '"'))
    email = json_data['email']
    password = json_data['password']
    db = MyUser()
    db.createUser(email, password)
    finalDict = db.getResult()
    print(finalDict)
    return finalDict

if __name__ == '__main__':
    app.run()