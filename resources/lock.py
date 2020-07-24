
import os

from flask_restful import Resource, reqparse


class Lock(Resource):
    """ Resource for locking/unlocking paths. """

    inaccessible = set()  # tohle by asi melo jit do databaze, ale delam jenom demo..
    parser = reqparse.RequestParser()
    parser.add_argument("filepath", type=str, required=True, help="path which will be inaccesible.")
    
    def post(self):
        """ Endpoint for locking a path so that it is not accessible. """
        data = Lock.parser.parse_args()
        Lock.inaccessible.add(data['filepath'])
        return {"message": f"path '{data['filepath']}' is inaccessible now."}, 200

    def delete(self):
        """ Endpoint for unlocking a path so that it is accessible again. """
        data = Lock.parser.parse_args()
        try:
            Lock.inaccessible.remove(data['filepath'])
            return {"message": f"path '{data['filepath']}' is accessible."}, 200
        except KeyError:
            return {"error": f"path '{data['filepath']}' not found."}, 404

    def get(self):
        """ Endpoint for seeing locked paths. """
        return {"inaccessible_paths": list(Lock.inaccessible)}, 200