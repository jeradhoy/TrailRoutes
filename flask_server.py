from flask import Flask
from flask import render_template
from flask_restful import reqparse, abort, Api, Resource
import psycopg2
import json

from routing_algo.trail_search import get_all_loops
from routing_algo.trail_search import get_point_to_point
# from routing_algo.trail_search import find_p2p_dfs

# conn = psycopg2.connect(dbname="trailDb", user="postgres", host="localhost", password="meow")
# #paths = get_point_to_point(conn, 23387, 23416, 30)

# find_p2p_dfs(conn, 23387, 23416, 30)

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

    def get(self, junct_id1, junct_id2, max_miles):

        print("Finding paths...")
        if junct_id2 == "null":
            paths = get_all_loops(self.conn, int(junct_id1), int(max_miles))
        else:
            paths = get_point_to_point(self.conn, int(junct_id1), int(junct_id2), int(max_miles))

        # return [
        #         {"trails": [5303, 5305, 5323], "dist": 5.5},
        #         {"trails": [5303, 5287, 5288], "dist": 4.9},
        #        ]
        print("Found paths, returning!")
        #print(paths)
        return paths[0:100]

api.add_resource(Routes, '/routes/<junct_id1>&<junct_id2>&<max_miles>')

# run the application
if __name__ == "__main__":
    
    # Change user who can access database
    app.run(host="0.0.0.0", port=80, debug=True)
    conn.close()