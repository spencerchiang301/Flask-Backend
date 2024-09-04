import configparser
from Utility.MyMariadb import MyMariadb

config = configparser.ConfigParser()
config.read('Setting/config.ini')


class MyUser:
    def __init__(self):
        self.user = config['MARIADB']['user']
        self.password = config['MARIADB']['password']
        self.host = config['MARIADB']['host']
        self.port = config['MARIADB']['port']
        self.db = config['MARIADB']['userDB']
        self.myToken = MyToken()
        self.mydb = MyMariadb(self.user, self.password, self.host, int(self.port), self.db)
        self.mydb.initConn()
        self.finalDict = {}

    def loginUser(self, userId, password):
        querySelect = "SELECT userId FROM user_register_info " \
                      f"WHERE userId = '{userId}' and password='{password}' " \
                      f"LIMIT 1;"
        self.mydb.query(querySelect)
        if self.mydb.cursor.rowcount != 1:
            (unixTimeStamp, unixDateTime, localDateTime) = self.myTime.getUnixTimeStamp()
            queryInsert = f"INSERT INTO user_action_info(userId, actionType,actionStatus, " \
                          f"actionContent, loginDateTime, loginTimeStamp) " \
                          f"VALUES ('{userId}','Login','Failed','user and password don''t match'," \
                          f"'{localDateTime}','{unixTimeStamp}');"
            self.mydb.InsertUpdateAndDelete(queryInsert)

            self.finalDict = {}
            self.finalDict["actionStatus"] = "Success"
            self.finalDict["loginStatus"] = "False"
            self.finalDict["responseTTS"] = "User and password don't match"
        else:
            queryUpdate = f"Update user_register_info SET loginStatus='True' " \
                          f"WHERE userId='{userId}' LIMIT 1;"
            self.mydb.InsertUpdateAndDelete(queryUpdate)
            (unixTimeStamp, unixDateTime, localDateTime) = self.myTime.getUnixTimeStamp()
            queryInsert = f"INSERT INTO user_action_info(userId, actionType, actionStatus," \
                          f"actionContent,loginDateTime,loginTimeStamp) VALUES " \
                          f"('{userId}','Login','Success','Authentication Success'," \
                          f"'{localDateTime}','{unixTimeStamp}');"
            self.mydb.InsertUpdateAndDelete(queryInsert)
            self.myToken.createToken(userId)
            access_token, refresh_token = self.myToken.getToken(userId)
            self.finalDict = {}
            self.finalDict["actionStatus"] = "Success"
            self.finalDict["loginStatus"] = "True"
            self.finalDict["userId"] = userId
            self.finalDict["access_token"] = access_token
            self.finalDict["refresh_token"] = refresh_token
            self.finalDict["responseTTS"] = f"user login success"

    def createUser(self, userId, password):
        userExist = self.checkUserExist(userId)
        if userExist is False:
            (unixTimeStamp, unixDateTime, localDateTime) = self.myTime.getUnixTimeStamp()
            queryInsert = f"INSERT INTO user_register_info(userId, password, registerTimeStamp, " \
                          f"registerDateTime, loginTimeStamp, loginDateTime, activateDate, " \
                          f"loginStatus, accountStatus ) " \
                          f"VALUES('{userId}','{password}','{unixTimeStamp}'," \
                          f"'{unixDateTime}','{unixTimeStamp}','{unixDateTime}'," \
                          f"'{localDateTime}','False','Enabled');"
            print(queryInsert)
            self.mydb.InsertUpdateAndDelete(queryInsert)
            queryInsert = f"INSERT INTO user_action_info(userId, actionType,  actionStatus," \
                          f"actionContent,loginDateTime,loginTimeStamp) VALUES " \
                          f"('{userId}','Created','Success','Create a new user succeed'," \
                          f"'{localDateTime}','{unixTimeStamp}');"
            print(queryInsert)
            self.mydb.InsertUpdateAndDelete(queryInsert)
            checkUser = self.checkUserExist(userId)

            if checkUser is False:
                self.finalDict = {}
                self.finalDict["actionStatus"] = "Failed"
                self.finalDict["userId"] = userId
                self.finalDict["responseTTS"] = f"Can't add user，please contact XXXX"
            else:
                self.myToken.createToken(userId)
                access_token, refresh_token = self.myToken.getToken(userId)
                self.finalDict = {}
                self.finalDict["actionStatus"] = "Success"
                self.finalDict["userId"] = userId
                self.finalDict["access_token"] = access_token
                self.finalDict["refresh_token"] = refresh_token
                self.finalDict["responseTTS"] = f"register a new user successfully"

    def checkUserExist(self, userId):
        userExist = False
        querySelect = f"SELECT * FROM user_register_info " \
                      f"WHERE userId = '{userId}';"
        self.mydb.query(querySelect)
        if self.mydb.cursor.rowcount != 0:
            self.finalDict = {}
            self.finalDict["actionStatus"] = "Failed"
            self.finalDict["userId"] = userId
            self.finalDict["responseTTS"] = f"The user exists and can't add again"
            userExist = True

        return userExist

    def updateUserInfo(self, userId, firstName, lastName, phone, contact1, contact2):
        queryUpdate = f"UPDATE user_register_info SET firstName ='{firstName}', " \
                      f"lastName='{lastName}', phone='{phone}', contact1='{contact1}'," \
                      f"contact2='{contact2}' WHERE userId='{userId}' LIMIT 1;"
        self.mydb.InsertUpdateAndDelete(queryUpdate)
        (unixTimeStamp, unixDateTime, localDateTime) = self.myTime.getUnixTimeStamp()
        queryInsert = f"INSERT INTO user_action_info(userId, actionType,  actionStatus, " \
                      f"actionContent, loginDateTime,loginTimeStamp) VALUES " \
                      f"('{userId}','Updated','Failed','Update user info succeed'," \
                      f"'{localDateTime}','{unixTimeStamp}');"
        self.mydb.InsertUpdateAndDelete(queryInsert)

        self.finalDict = {}
        self.finalDict["actionStatus"] = "Success"
        self.finalDict["responseTTS"] = f"update user info succeed"

    def refreshToken(self, userId):
        querySelect = f"SELECT * FROM user_register_info " \
                      f"WHERE userId = '{userId}' " \
                      f"AND accountStatus='Enabled';"
        self.mydb.query(querySelect)
        self.finalDict = {}
        if self.mydb.cursor.rowcount != 0:
            access_token = self.myToken.refreshToken(userId)
            self.finalDict["actionStatus"] = "Success"
            self.finalDict["userId"] = userId
            self.finalDict["access_token"] = access_token
        else:
            self.finalDict["actionStatus"] = "Success"
            self.finalDict["responseTTS"] = f"This user account is disabled"

    def getLogout(self, userId):
        queryUpdate = f"UPDATE user_token SET token_status='disabled' " \
                      f"WHERE userId='{userId}' LIMIT 1;"
        self.mydb.InsertUpdateAndDelete(queryUpdate)

        self.finalDict = {}
        self.finalDict["actionStatus"] = "Success"
        self.finalDict["responseTTS"] = f"User had logout"

    def updatePassword(self, userId, oldPassword, newPassword):
        userExist = self.checkUserExist(userId)
        if userExist:
            queryUpdate = f"UPDATE user_register_info SET password='{newPassword}' " \
                          f"WHERE userId='{userId}' and password='{oldPassword}' LIMIT 1;"
            self.mydb.InsertUpdateAndDelete(queryUpdate)

            (unixTimeStamp, unixDateTime, localDateTime) = self.myTime.getUnixTimeStamp()
            queryInsert = f"INSERT INTO user_action_info(userId, actionType,  actionStatus, " \
                          f"actionContent, loginDateTime,loginTimeStamp) VALUES " \
                          f"('{userId}','Update Password','Success','Update user''s password succeed'," \
                          f"'{localDateTime}','{unixTimeStamp}');"
            self.mydb.InsertUpdateAndDelete(queryInsert)
            self.finalDict = {}
            self.finalDict["actionStatus"] = "Success"
            self.finalDict["responseTTS"] = f"update user password succeed"
        else:
            (unixTimeStamp, unixDateTime, localDateTime) = self.myTime.getUnixTimeStamp()
            queryInsert = f"INSERT INTO user_action_info(userId, actionType,  actionStatus," \
                          f"actionContent, loginDateTime,loginTimeStamp) VALUES " \
                          f"('{userId}','Update Password','Failed','Update user''s password failed'," \
                          f"'{localDateTime}','{unixTimeStamp}');"
            self.mydb.InsertUpdateAndDelete(queryInsert)
            self.finalDict = {}
            self.finalDict["actionStatus"] = "Success"
            self.finalDict["responseTTS"] = f"upate user password failed"

    def updateRescueInfo(self, userId, phone, contact1, contact2):
        userExist = self.checkUserExist(userId)
        if userExist:
            querySelect = f"SELECT phone, name FROM user_phone_book " \
                          f"WHERE name ='{contact1}' AND userId='{userId}' UNION " \
                          f"SELECT phone, name FROM user_phone_book " \
                          f"WHERE name ='{contact2}' AND userId='{userId}';"
            self.mydb.query(querySelect)
            contact1Phone = ''
            contact2Phone = ''
            counter = 0
            for item in self.mydb.cursor:
                if counter == 0:
                    contact1Phone = item[0]
                else:
                    contact2Phone = item[0]
                counter += 1
            queryUpdate = f"UPDATE user_register_info SET phone='{phone}'," \
                          f"contact1='{contact1}',contact1Phone='{contact1Phone}'," \
                          f"contact2='{contact2}',contact2Phone='{contact2Phone}' " \
                          f"WHERE userId='{userId}' LIMIT 1;"
            print(queryUpdate)
            self.mydb.InsertUpdateAndDelete(queryUpdate)

            (unixTimeStamp, unixDateTime, localDateTime) = self.myTime.getUnixTimeStamp()
            queryInsert = f"INSERT INTO user_action_info(userId, actionType,  actionStatus, " \
                          f"actionContent, loginDateTime,loginTimeStamp) VALUES " \
                          f"('{userId}','Update rescue','Success','Update rescue''s information succeed'," \
                          f"'{localDateTime}','{unixTimeStamp}');"

            self.mydb.InsertUpdateAndDelete(queryInsert)
            self.finalDict = {}
            self.finalDict["actionStatus"] = "Success"
            self.finalDict["responseTTS"] = f"Get RescueInfo succeed"
        else:
            (unixTimeStamp, unixDateTime, localDateTime) = self.myTime.getUnixTimeStamp()
            queryInsert = f"INSERT INTO user_action_info(userId, actionType,  actionStatus," \
                          f"actionContent, loginDateTime,loginTimeStamp) VALUES " \
                          f"('{userId}',Update rescue','Failed','Update rescue's information failed'," \
                          f"'{localDateTime}','{unixTimeStamp}');"
            self.mydb.InsertUpdateAndDelete(queryInsert)
            self.finalDict = {}
            self.finalDict["actionStatus"] = "Success"
            self.finalDict["responseTTS"] = f"Failed to get RescueInfo"


    def getResult(self):
        return self.finalDict