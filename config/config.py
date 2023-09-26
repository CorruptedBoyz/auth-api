import os

def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@Singleton
class Configuration:
    mongo_host: str
    port: int
    secret: str

    def __init__(self):
        self.mongo_host = os.environ.get("MONGO_HOST", "localhost")
        self.port = int(os.environ.get("PORT", "5000"))
        self.secret = os.environ.get("SECRET", "secret")

