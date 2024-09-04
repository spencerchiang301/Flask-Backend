import uuid


class MyMisc:
    def __init__(self):
        pass

    def getUniqueId(self):
        return uuid.uuid1()