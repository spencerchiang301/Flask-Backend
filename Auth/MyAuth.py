import configparser

from flask_jwt_extended import create_access_token, \
    create_refresh_token, get_jti

from Utility.MyMariadb import MyMariadb
from Utility.MyTime import MyTime

config = configparser.ConfigParser()
config.read('Setting/config.ini')


class MyToken:

    def __init__(self):
        self.user = config['MARIADB']['user']
        self.password = config['MARIADB']['password']
        self.host = config['MARIADB']['host']
        self.port = config['MARIADB']['port']
        self.db = config['MARIADB']['userDB']
        self.myTime = MyTime()
        self.mydb = MyMariadb(self.user, self.password, self.host, int(self.port), self.db)
        self.mydb.initConn()
        self.finalDict = {}

    def createToken(self, userId):

        # set all access_token and refresh_token status to disabled
        queryUpdate = f"UPDATE user_access_token SET token_status ='disabled' " \
                      f"WHERE userId='{userId}' and token_status='enabled';"
        self.mydb.InsertUpdateAndDelete(queryUpdate)
        queryUpdate = f"UPDATE user_refresh_token SET token_status ='disabled' " \
                      f"WHERE userId='{userId}' and token_status='enabled';"
        self.mydb.InsertUpdateAndDelete(queryUpdate)

        # create new access token and refresh token for userId
        access_token = create_access_token(identity=userId)
        access_token_jti = get_jti(access_token)
        refresh_token = create_refresh_token(identity=userId)
        refresh_token_jti = get_jti(refresh_token)

        # Insert new token info
        queryInsert = f"INSERT INTO user_access_token(userId, access_token, " \
                      f"access_token_jwi, token_status) values('{userId}','{access_token}'," \
                      f"'{access_token_jti}','enabled');"
        # print(queryInsert)
        self.mydb.InsertUpdateAndDelete(queryInsert)
        queryInsert = f"INSERT INTO user_refresh_token(userId, refresh_token, " \
                      f"refresh_token_jwi, token_status) values('{userId}','{refresh_token}'," \
                      f"'{refresh_token_jti}','enabled');"
        # print(queryInsert)
        self.mydb.InsertUpdateAndDelete(queryInsert)

    def getToken(self, userId):
        # get new token
        querySelect = f"SELECT a.access_token, r.refresh_token " \
                      f"FROM user_access_token as a " \
                      f"LEFT JOIN user_refresh_token as r " \
                      f"ON a.userId = r.userId " \
                      f"WHERE a.userId = '{userId}' AND a.token_status='enabled' " \
                      f"AND r.token_status ='enabled';"
        print(querySelect)
        self.mydb.query(querySelect)
        if self.mydb.cursor.rowcount != 0:
            for item in self.mydb.cursor:
                access_token = item[0]
                refresh_token = item[1]
                return access_token, refresh_token
        else:
            return 'Failed', 'Failed'

    def refreshToken(self, userId):
        queryUpdate = f"UPDATE user_access_token SET token_status = 'disabled' " \
                      f"WHERE userId = {userId} and token_status = 'enabled';"
        self.mydb.InsertUpdateAndDelete(queryUpdate)

        access_token = create_access_token(identity=userId)
        access_token_jti = get_jti(access_token)
        queryInsert = f"INSERT INTO user_access_token(userId, access_token, " \
                      f"access_token_jti,token_status VALUES('{userId}'," \
                      f"'{access_token}','{access_token_jti}','enabled');"
        self.mydb.InsertUpdateAndDelete(queryInsert)
        return access_token

    def revokeToken(self, userId):
        queryUpdate = f"UPDATE user_access_token SET token_status = 'disabled' " \
                      f"WHERE userId = {userId} LIMIT 1;"
        self.mydb.InsertUpdateAndDelete(queryUpdate)
        queryUpdate = f"UPDATE user_refresh_token SET token_status = 'disabled' " \
                      f"WHERE userId = {userId} LIMIT 1;"
        self.mydb.InsertUpdateAndDelete(queryUpdate)