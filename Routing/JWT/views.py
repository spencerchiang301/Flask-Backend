from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from Module.Auth.MyUser import MyUser
import redis
jwt = JWTManager()

jwt_blueprints = Blueprint('jwt', __name__)
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


@jwt_blueprints.route("/checkTokenRevoked", methods=['POST'])
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@jwt_blueprints.route("/refreshToken", methods=['POST'])
@jwt_required(refresh=True)
def getRefreshToken():
    identity = get_jwt_identity()
    db = MyUser()
    db.refreshToken(identity)
    finalDict = db.getResult()
    return finalDict