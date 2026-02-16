from flask import Flask
from config import LocalDevelopmentConfig
from extensions import db
import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    # initialize database
    db.init_app(app)

    # create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
