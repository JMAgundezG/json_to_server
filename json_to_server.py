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
            Example: http http://localhost:5000 user:='{"name": "john", "age": 10 }
        """

        json_data = request.get_json(force=True)
        if json_data is not None:
            key = list(json_data.keys())[0]
            db[key] = json_data[key]
            return "[INFO] CREATED", 201
        else:
            return "[ERROR] INTERNAL SERVER ERROR", 500


class TableRest(Resource):
    """
        All the API refered to the tables.
        URL: http://localhost:5000/<table_name>

    """

    def get(self, key):
        """ 
        Returns the table named key
        """
        if key in db.keys():
            return db[key], 200
        else:
            return "[ERROR] "+ key + " TABLE DOESN'T EXISTS", 404

    def post(self, key):
        """
            Post a tuple into the $key table.
            If you use an already created tuple you can't post it
            Example: http http://localhost:5000/users :='{"name": "john", "age": 10 }
        """
        if key not in db.keys():
            return "[ERROR] "+ key + " TABLE DOESN'T EXISTS", 404
        json_data = request.get_json(force=True)
        if json_data is not None:
            ik = list(json_data.keys())[0]
            data = json_data[ik]
            if type(data) == dict:
                if len(db[key]) == 0: 
                    db[key].append(data)
                    return "[INFO] ACCEPTED", 201
                elif data.keys() == db[key][0].keys():
                    if len(list(filter(lambda x: x["id"] == data["id"], db[key]))) == 0:
                        db[key].append(data)
                        return "[INFO] ACCEPTED", 201
                else:
                    return "[ERROR] WRONG COLUMNS FOR THAT TABLE", 403 
            else:
                return "[ERROR] INTERNAL SERVER ERROR", 500
        return "[ERROR] INTERNAL SERVER ERROR", 500



    def delete(self, key):
        """
            Deletes a table if it exists
        """
        print("[INFO] Trying to delete "+key+" table")
        if key in db.keys():
            print("[INFO] deleted "+key+" table")
            del db[key]
            return "[INFO] deleted "+key+" table", 200
        else:
            print("[INFO] "+key+" table doesn't exists")
            return "[ERROR] "+ key + " TABLE DOESN'T EXISTS", 404


class TupleRest(Resource):
    """
        All the API refered to tuples
        URL: http://localhost:5000/<table>/<id>
    """

    def get(self, table, key):
        """
            Get the tuple with id=$key from the table=$table 
        """
        if table in db.keys():
            id = 'id'
            tuples = list(filter(lambda x: (x[id] == key), db[table]))
            return tuples[0], 200

    def post(self, table, key):
        """
            Post a tuple into the $key table.
            If you use an already created tuple you can't post it
            The key variable is useless ¯\_(ツ)_/¯ 
            Example: http http://localhost:5000/users/0 :='{"name": "john", "age": 10 }
        """
        if table not in db.keys():
           return "[ERROR] "+ key + " TABLE DOESN'T EXISTS", 404

        json_data = request.get_json(force=True)
        if json_data is not None:
            ik = list(json_data.keys())[0]
            data = json_data[ik]
            if type(data) == dict:
                if len(db[key]) == 0: 
                    db[key].append(data)
                    return 201
                elif data.keys() == db[key][0].keys():
                    if len(list(filter(lambda x: x["id"] == data["id"], db[table]))) == 0:
                        db[key].append(data)
                else:
                    return "[ERROR] WRONG COLUMNS FOR THAT TABLE", 403 
            else:
                return "INTERNAL SERVER ERROR", 500
        return "INTERNAL SERVER ERROR", 500
    
    def put(self, table, key):
        """
        """
        if table not in db.keys():
            return "[ERROR] "+ key + " TABLE DOESN'T EXISTS", 500

        json_data = request.get_json(force=True)
        if json_data is not None:
            ik = list(json_data.keys())[0]
            data = json_data[ik]
            if type(data) == dict:
                if data.keys() == db[key][0].keys():
                    if len(list(filter(lambda x:["id"] == data["id"], db[table]))) == 1:
                        data["id"] = list(filter(lambda x:["id"] != data["id"], db[table]))
                else:
                    return "[ERROR] WRONG COLUMNS FOR THAT TABLE", 403 
            else:
                return "INTERNAL SERVER ERROR", 500
        return "INTERNAL SERVER ERROR", 500


    def delete(self, table, key):
        """
            Delete the tuple with id=$key from the table=$table 
        """
        if table in db.keys():
            id = 'id'
            removed = list(filter(lambda x: (x[id] == key), db[table]))
            if len(removed) > 0:
                db[table] = list(filter(lambda x: (x[id] != key), db[table]))
            return 200
        else:
             return "[ERROR] "+ key + " TABLE DOESN'T EXISTS", 500

    

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
        

