import os

from flask import current_app as app
from flask_restful import Resource, reqparse, request

from utils import get_details
from resources.lock import Lock


class File(Resource):
    """ Resource for one file/folder. """

    parser = reqparse.RequestParser()
    parser.add_argument("filename", type=str, required=True, help="name of the file")
    current_path = ''

    def get(self, path: str):
        """ Endpoint for viewing single file. """
        path = os.path.join(os.sep, path)
        File.current_path = request.path
        if path in Lock.inaccessible:
            return {"error": f"path '{path}' is innacessible."}, 403

        try:
            return get_details(path), 200
        except FileNotFoundError:
            return {"error": f"path '{path}' does not exist!"}, 404

    def delete(self, path: str):
        """ Endpoint for deleting a file or empty folder. """
        filename = File.parser.parse_args()  # /myfile.txt
        filepath = os.path.join(os.sep, path, filename["filename"])  # /home/lukas/myfile.txt
        if os.path.join(os.sep, path) in Lock.inaccessible:
            return {"error": f"path '{path}' is innacessible."}, 403

        if os.path.exists(filepath):
            if os.path.isfile(filepath):
                try:
                    os.remove(filepath)
                    return {"messsage": f"file '{filepath}' deleted!"}, 200
                except PermissionError:
                    return {"error": f"no permission to remove file '{filepath}'"}, 403
            elif os.path.isdir(filepath):
                try:
                    if not os.listdir(filepath):
                        os.rmdir(filepath)
                        return {"messsage": f"directory '{filepath}' deleted!"}, 200
                    else:
                        return {"error": f"directory '{filepath}' is not empty - cannot be deleted"}, 400
                except PermissionError:
                    return {"error": f"no permission to remove directory '{filepath}'"}, 403
        return {"error": f"path '{filepath}' does not exist!"}, 404

    def post(self, path: str):
        """ Endpoint for creating a file or directory. """
        filename = File.parser.parse_args()  # /myfile.txt
        filepath = os.path.join(os.sep, path, filename["filename"])  # /home/lukas/myfile.txt
        if os.path.join(os.sep, path) in Lock.inaccessible:
            return {"error": f"path '{path}' is innacessible."}, 403

        if not os.path.exists(os.path.join(os.sep, path)):
            return {"error": f"path '{path}' does not exist!"}, 404

        try:
            if os.path.exists(filepath):
                return {"message": f"file '{filepath}' already existed."}, 204
            else:
                with open(filepath, "w"):
                    pass
                return {"message": f"file '{filepath}' created."}, 200
        except PermissionError:
            return {"error": f"no permission to create file in directory '{path}'"}, 403