from pymongo import MongoClient
from pymongo.database import Database
from config.config import Configuration


class Client:

    client: Database

    def __init__(self):
        self.client = None

    def get_client(self) -> Database:
        if self.client is None:
            config = Configuration()
            self.client = MongoClient(
                f"mongodb://{config.mongo_host}:27017/").get_database("shooter")
        return self.client
