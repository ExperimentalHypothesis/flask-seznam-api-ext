import markdown, os

from flask import Flask, request
from flask_restful import Api

from resources.file import File
from resources.files import Files
from resources.lock import Lock

app = Flask(__name__)


@app.route("/")
def index():
    """ Route to index page for displaing documentation. """
    with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as md:
        content = md.read()
        return markdown.markdown(content)


@app.before_request
def before_request():
    """ Disable access to parrent folders. """
    if request.path == os.path.dirname(File.current_path) or request.path == os.path.dirname(Files.current_path):
        return {"error": "you cannnot move to upper directory."}


api = Api(app)
api.add_resource(File, "/file/<path:path>")
api.add_resource(Files, "/files/<path:path>")
api.add_resource(Lock, "/lock")


if __name__ == "__main__":
    app.run(debug=True)
