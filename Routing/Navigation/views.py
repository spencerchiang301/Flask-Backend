from datetime import datetime
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from werkzeug.utils import secure_filename

from MyFile import MyFile
from Routing.Navigation.MyNavigation import MyNavigation

jwt = JWTManager()

navigation_blueprints = Blueprint('navigation', __name__)

@navigation_blueprints.route('/getNavigationFile', methods=['POST'])
@jwt_required()
def getNavigationFile():
    target = "./temp"
    words = request.form['words']
    file = request.files['file']
    filename = secure_filename(file.filename)
    today = datetime.utcnow()
    unixTimeStamp = str(today.timestamp())[0:10]
    filename = "-".join([unixTimeStamp, filename])
    destination = "/".join([target, filename])
    file.save(destination)
    db = MyFile()
    db.changeUserId(words)
    db.changeFile(filename)
    db.writeToNavigation()
    finalDict = db.getResult()
    return finalDict


@navigation_blueprints.route('/getNavigation', methods=['POST'])
@jwt_required()
def getNavigation():
    words = request.get_json()['words']
    if words == get_jwt_identity():
        db = MyNavigation()
        db.changeUserId(words)
        db.getAllNavigation()
        return db.getResult()


@navigation_blueprints.route('/addNavigation', methods=['POST'])
@jwt_required()
def addNavigation():
    words = request.get_json()['words']
    name = request.get_json()['name']
    address = request.get_json()['address']
    if words == get_jwt_identity():
        db = MyNavigation()
        db.changeUserId(words)
        db.addNavigation(name, address)
        finalDict = db.getResult()
        return finalDict
    else:
        finalDict = {}
        finalDict["responseTTS"] = "Token is inValid"
        return finalDict


@navigation_blueprints.route('/updateNavigation', methods=['POST'])
@jwt_required()
def updateNavigation():
    words = request.get_json()['words']
    preName = request.get_json()['preName']
    preAddress = request.get_json()['preAddress']
    name = request.get_json()['name']
    address = request.get_json()['address']
    print(f"{words}-{preName}-{name}-{preAddress}-{address}")
    if words == get_jwt_identity():
        db = MyNavigation()
        db.changeUserId(words)
        db.updateNavigation(preName, preAddress, name, address)
        finalDict = db.getResult()
        return finalDict
    else:
        finalDict = {}
        finalDict["responseTTS"] = "Token is inValid"
        return finalDict


@navigation_blueprints.route('/deleteNavigation', methods=['POST'])
@jwt_required()
def deleteNavigation():
    words = request.get_json()['words']
    preName = request.get_json()['preName']
    preAddress = request.get_json()['preAddress']
    print(f"{words}-{preName}-{preAddress}")
    if words == get_jwt_identity():
        db = MyNavigation()
        db.changeUserId(words)
        db.deleteNavigation(preName, preAddress)
        finalDict = db.getResult()
        return finalDict
    else:
        finalDict = {}
        finalDict["responseTTS"] = "Token is inValid"
        return finalDict


@navigation_blueprints.route('/deleteAllNavigation', methods=['POST'])
@jwt_required()
def deleteAllNavigation():
    words = request.get_json()['words']
    if words == get_jwt_identity():
        db = MyNavigation()
        db.changeUserId(words)
        db.deleteAllNavigation()
        finalDict = db.getResult()
        return finalDict
    else:
        finalDict = {}
        finalDict["responseTTS"] = "Token is inValid"
        return finalDict