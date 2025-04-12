from flask import Flask
import os
from app.extensions import db, bcrypt, jwt, migrate
from datetime import timedelta

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object("config.Config")

    # --- JWT Configuration for Cookies ---
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]  # Use cookies to store JWT
    app.config["JWT_ACCESS_COOKIE_PATH"] = "/"     # Cookie path affects the entire site
    app.config["JWT_REFRESH_COOKIE_PATH"] = "/"    # If using refresh tokens
    app.config["JWT_COOKIE_SECURE"] = False        # Set to True if using HTTPS (RECOMMENDED for production)
    app.config["JWT_COOKIE_HTTPONLY"] = True       # Prevent JS access to the token cookie (security)
    app.config["JWT_COOKIE_SAMESITE"] = "Lax"      # CSRF protection ('Strict', 'Lax', 'None') - 'Lax' is a good default
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1) # Example expiration time

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    from app.routes import auth_bp  
    app.register_blueprint(auth_bp)

    return app