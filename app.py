import markdown, os

from flask import Flask
from flask_restful import Api

from resources.file import File
from resources.files import Files

app = Flask(__name__)

@app.route("/")
def index():
    """ Route to index page for displaing documentation. """
    with open(os.path.join(os.path.dirname(__file__), "README.md"), "r") as md:
        content = md.read()
        return markdown.markdown(content)


api = Api(app)
api.add_resource(File, "/file/<path:path>")
api.add_resource(Files, "/files/<path:path>")


if __name__ == "__main__":
    app.run(debug=True)
