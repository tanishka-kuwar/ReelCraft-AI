from flask import Flask

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "user_uploads"

from routes import *

if __name__ == "__main__":
    app.run(debug=True)