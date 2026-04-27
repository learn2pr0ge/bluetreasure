import os
from flask import Flask
from src.webfront import webstart
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(webstart)

if __name__ == '__main__':
    app.run()


