from flask import Flask
from flask import render_template
from flask_restful import reqparse, abort, Api, Resource
import psycopg2

from routing_algo.trail_search import get_all_loops

#import database

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
    
    def __init__(self):
        self.conn = psycopg2.connect(dbname="trailDb", user="postgres", host="localhost", password="meow")

    def get(self, junct_id, max_miles):
        print(junct_id)
        print(max_miles)
        loops = get_all_loops(self.conn, int(junct_id), int(max_miles))
        # return [
        #         {"trails": [5303, 5305, 5323], "dist": 5.5},
        #         {"trails": [5303, 5287, 5288], "dist": 4.9},
        #        ]
        return loops

api.add_resource(Routes, '/routes/<junct_id>&<max_miles>')

# run the application
if __name__ == "__main__":

    # Change user who can access database
    app.run(host="0.0.0.0", port=80, debug=True)
    conn.close()