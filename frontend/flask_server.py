from flask import Flask
from flask import render_template
from flask_restful import reqparse, abort, Api, Resource

# creates a Flask application, named app
app = Flask(__name__)
api = Api(app)

# a route where we will display a welcome message via an HTML template
@app.route("/")
def hello():
    return render_template('index.html')


#parser = reqparse.RequestParser()
#parser.add_argument('task')

class Routes(Resource):
    def get(self, junct_id):
        return {"path": [1, 2, 3, 4], "dist": 2.4}

api.add_resource(Routes, '/routes/<junct_id>')

# run the application
if __name__ == "__main__":
    app.run(debug=True)