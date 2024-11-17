from flask import Flask

from app.db import create_db
from app.routes.tour import tour_blueprint


app = Flask(__name__)
app.register_blueprint(tour_blueprint)


def main():
    create_db()
    app.run(debug=True, port=80)