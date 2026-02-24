from flask import Flask
from config import LocalDevelopmentConfig
from extensions import db,security
from models import User, Role
from flask_security.datastore import SQLAlchemyUserDatastore
from resources import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)

    # initialize database
    db.init_app(app)
    datastore=SQLAlchemyUserDatastore(db,User,Role)
    security.init_app(app,datastore)

    app.datastore=datastore

    app.register_blueprint(auth_bp)

    # create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
