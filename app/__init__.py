from flask import Flask
import os
from app.extensions import db, bcrypt, jwt, migrate

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.routes import auth_bp  
    app.register_blueprint(auth_bp)

    return app