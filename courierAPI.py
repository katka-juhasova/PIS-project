from flask import Flask
from flask_restful import Resource, Api
from flask import jsonify
from random import randint


app = Flask(__name__)
api = Api(app)


# returns successful courier reservation with 20% probability
class Courier(Resource):
    def get(self, courier_id):
        success = randint(1, 100) > 80

        result = {'success': success}
        return jsonify(result)


api.add_resource(Courier, '/courier/<courier_id>')


if __name__ == '__main__':
    app.run(port='5000')
