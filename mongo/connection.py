from pymongo.mongo_client import MongoClient

client = MongoClient("localhost", 27017)
db = client.kahoot
player_collection = db.get_collection("players")
room_collection = db.get_collection("rooms")


class Players:
    def __init__(self, id, host_id, game_data):
        self.id = id
        self.host_id = host_id
        self.game_data = game_data


class Rooms:
    def __init__(self, id, host_id, is_live, game_data):
        self.id = id
        self.host_id = host_id
        self.is_live = is_live
        self.game_data = game_data
