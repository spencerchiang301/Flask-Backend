import configparser
from Utility.MyMariadb import MyMariadb
from math import ceil

config = configparser.ConfigParser()
config.read('Setting/config.ini')


class MySera:
    def __init__(self):
        self.user = config['MARIADB']['user']
        self.password = config['MARIADB']['password']
        self.host = config['MARIADB']['host']
        self.port = config['MARIADB']['port']
        self.db = config['MARIADB']['db']
        self.mydb = MyMariadb(self.user, self.password, self.host, int(self.port), self.db)
        self.mydb.initConn()

    def add_product(self, json):
        sqlInsert = ""
        self.mydb.InsertUpdateAndDelete(sqlInsert)

    def readFileForRockery(self, fileName):
        sqlInsert = f"TRUNCATE TABLE SeraRockery;"
        self.mydb.InsertUpdateAndDelete(sqlInsert)
        with open(fileName, 'r', encoding='UTF-8') as f:
            for line in f.readlines():
                lineList = line.split("/")
                name = lineList[1]
                id = lineList[0]
                size = lineList[3]
                oriPrice = lineList[4].replace(",","")
                finalPrice=int(ceil((int(oriPrice)*1.3)/10)*10)
                print("{},{},{},{},{}".format(name,id,  size, oriPrice, finalPrice))
                sqlInsert = f"INSERT INTO SeraRockery(name, id, size, ori_price, price) " \
                            f"VALUES('{name}','{id}','{size}','{oriPrice}','{finalPrice}');"
                self.mydb.InsertUpdateAndDelete(sqlInsert)

a = MySera()
# a.readFileForProduct("Sera/sera.txt")
a.readFileForRockery("Sera/rockery.txt")
