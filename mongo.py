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

    def verify(self, disco, osu, verify_map, timestamp):
        mydict = {"discordId": disco, "osuId": osu, "connected": False, "map" : verify_map, "timestamp" : timestamp}
        self.mycol.insert_one(mydict)
        
    def add_user(self, disco, osu):
        mydict = { "discordId" : disco, "osuId" : osu}
        newvalue = { "$unset": {"map" : 1, "timestamp" : 1}, "$set" : {"connected" : True}}
        self.mycol.update_one(mydict, newvalue)

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