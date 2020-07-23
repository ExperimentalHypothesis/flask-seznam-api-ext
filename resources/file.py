import os

from flask_restful import Resource

from utils import get_details


class File(Resource):
    """ Resource for one file/folder. """

    def get(self, path: str):
        """ Endpoint for viewing single file. """
        path = "/" + path
        # if path not in unlocked_paths:
        #     return jsonify({"error": f"path '{path}' is locked, if you want to see its details, authenticate it first."})
        try:
            return get_details(path), 200
        except FileNotFoundError:
            return {"error": f"path '{path}' is invalid!"}, 404

    def delete(self, path: str):
        """ Endpoint for deleting a file or empty folder. """
        path = "/" + path
        if os.path.exists(path):
            if os.path.isfile(path):
                try:
                    os.remove(path)
                    return {"messsage": f"file '{path}' deleted!"}, 200
                except PermissionError:
                    return {"error": f"no permission to remove file '{path}'"}, 400
            elif os.path.isdir(path):
                try:
                    if not os.listdir(path):
                        os.rmdir(path)
                        return {"messsage": f"directory '{path}' deleted!"}, 200
                    else:
                        return {"error": f"directory '{path}' is not empty - cannot be deleted"}, 404
                except PermissionError:
                    return {"error": f"no permission to remove directory '{path}'"}, 400
        return {"error": f"path '{path}' is invalid!"}, 404

