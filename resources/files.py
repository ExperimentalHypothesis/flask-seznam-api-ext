import os

from flask_restful import Resource

from utils import get_details


class Files(Resource):
    """ Resource for multiple files/folders. """

    def get(self, path: str):
        """ Endpoint for listing all file/folders in specified path. """
        path = "/" + path
        # if path not in unlocked_paths:
        #     return {"error": f"path '{path}' is locked, if you want to see its details, authenticate it first."}
        try:
            files = [get_details(os.path.join(path, file)) for file in os.listdir(path)]
            return {"files": files}, 200
        except FileNotFoundError:
            return {"error": f"path '{path}' is invalid!"}, 404
   