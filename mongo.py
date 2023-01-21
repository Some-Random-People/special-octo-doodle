import pymongo
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Mon:
    def __init__(self):
        self.mycol = None
        self.mydb = None

    def connect(self):
        try:
            client = pymongo.MongoClient(os.getenv("CONN_STR"), serverSelectionTimeoutMS=5000)
            self.mydb = client["SpecialOctoDoodle"]
            self.mycol = self.mydb["users"]
        except Exception:
            print("Unable to connect to the server.")

    def add_user(self, disco, osu):
        mydict = { "discordId" : disco, "osuId" : osu, "connected" : True }
        self.mycol.insert_one(mydict)

    def check_user_discord(self, discordId):
        myquery = { "discordId" : discordId}
        x = self.mycol.find(myquery,{"_id" : 0})
        result = None
        print(x)
        for i in x:
            result = i
        if result:
            return result
        else:
            return False
    def check_user_osu(self, osuId):
        myquery = { "osuId" : osuId}
        x = self.mycol.find(myquery,{"_id" : 0})
        result = None
        for i in x:
            result = i
        if result:
            return result
        else:
            return False
    def asd(self):
        mydict = {}
        try:
            self.mycol.insert_one(mydict)
            return self.mydb.list_collection_names()
        except Exception:
            print("Unable to connect to the server.")