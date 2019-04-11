from flask import Flask, request
from flask_restful import Resource, Api
import sys
import json
import xml
db = {}

"""
    url:'localhost:5000/'
    Main rest.
    GET: Returns all the BD
    POST: 
    DELETE: Erase a main json key
"""
class MainRest(Resource):
    def get(self):
        """ 
        Returns all the db
        """
        return db, 200

    def delete(self):
        """
        Remove a table from the DB
        Example: DELETE http://localhost:5000/?key=profile
        """

        name = request.args.get('key')
        print("[INFO] Trying to delete "+name+" table")
        if name in db.keys():
            del db[name]
            print("[INFO] deleted "+name+" table")
            return "[INFO] deleted "+name+" table", 200
        else:
            print("[INFO] "+name+" table doesn't exists")
            return "[INFO] "+name+" table doesn't exists", 404
    
    def post(self):
        """
            Input a table into the DB.
            If you use an already created table you will erase it
            Example: http httpbin.org/post user:='{"name": "john", "age": 10 }
        """

        db[]


class TableRest(Resource):
    def get(self, key):
        if key in db.keys():
            return db[key], 200
        else:
            return "[INFO] "+key+" table doesn't exists"

    def post(self, key):
        pass

    def delete(self, key):
        print("[INFO] Trying to delete "+key+" table")
        if key in db.keys():
            print("[INFO] deleted "+key+" table")
            del db[key]
            return "[INFO] deleted "+key+" table", 200
            
        else:
            print("[INFO] "+key+" table doesn't exists")
            return "[INFO] "+ key +" table doesn't exists", 404


class TupleRest(Resource):
    def get(self, table, key):
        if table in db.keys():
            id = 'id'
            tuples = list(filter(lambda x: (x[id] == key), db[table]))
            return tuples, 200
    

class ApiServer:
    def __init__(self, db):
        self.db = db
        self.app = Flask(__name__)
        self.api = Api(self.app)
    
    def start(self):
        self.api.add_resource(MainRest, '/')
        self.api.add_resource(TableRest, '/<string:key>')
        self.api.add_resource(TupleRest, '/<string:table>/<string:key>')

        self.app.run(debug=True)

def some_help():
    pass

if __name__ == '__main__':
    if len(sys.argv) == 1:
        some_help()
        exit(0)
    else:

        db = json.load(open(sys.argv[1]))
        ApiServer(db).start()
        

