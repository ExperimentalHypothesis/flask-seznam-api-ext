import os

from flask import request
from flask_restful import Resource

from utils import get_details
from resources.lock import Lock


class Files(Resource):
    """ Resource for multiple files/folders. """

    current_path = ''
    
    def get(self, path: str):
        """ Endpoint for listing all file/folders in specified path. """
        path = os.path.join(os.sep, path)
        Files.current_path = request.path
        if path in Lock.inaccessible:
            return {"error": f"path '{path}' is innacessible."}, 403

        try:
            files = [get_details(os.path.join(path, file)) for file in os.listdir(path)]
            return {"files": files}, 200
        except FileNotFoundError:
            return {"error": f"path '{path}' does not exist!"}, 404
        except NotADirectoryError:
            return {"error": f"path '{path}' is file, not directory!"}, 400
     