from flask import Flask, request, jsonify, make_response
import jwt
from db.mongodb import Client
from config.config import Configuration
import random


class FlaskAppWrapper:

    def __init__(self, app: Flask):
        self.app = app
        self.collection = Client().get_client().get_collection("users")
        self.config = Configuration()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name,
                              handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        print(self.config.port)
        self.app.run(**kwargs, port=self.config.port, debug=True, host="0.0.0.0")

    def register(self):
        form = request.get_json()
        username, password = form.get('username'), form.get('password')

        self.collection.insert_one({
            "username": username,
            "password": password
        })

        return "Success"

    def login(self):
        form = request.get_json()

        username, password = form.get('username'), form.get('password')
        user = self.collection.find_one({
            "username": username,
            "password": password
        })

        if not user:
            return make_response('User not found', 404)
        else:
            encoded_jwt = jwt.encode(
                {"username": username}, self.config.secret, algorithm="HS256")
            return make_response(jsonify({"token": encoded_jwt}), 202)

    def test(self):
        form = request.get_json()

        token = form.get('token')
        encoded_jwt = jwt.decode(token, self.config.secret, algorithms=["HS256"])

        return make_response(jsonify({"token": encoded_jwt, "random": random_string}), 202)

random_string = random.randint(0,9999)
flask_app = Flask(__name__)
app = FlaskAppWrapper(flask_app)
app.add_endpoint("/register", "register", app.register, methods=['POST'])
app.add_endpoint("/login", "login", app.login, methods=['POST'])
app.add_endpoint("/test", "test", app.test, methods=['POST'])
if __name__ == "__main__":
    app.run()
