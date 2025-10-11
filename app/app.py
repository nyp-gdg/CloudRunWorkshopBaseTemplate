import os
from flask import Flask,  jsonify
from .db import init_db
from .auth import bp as auth_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    ## For future integrations into Google Secret Manager API ^
    init_db()

    @app.get("/")
    def index():
        return jsonify({"ok" : True, "service": "cloud-run-flask"})
    
    app.register_blueprint(auth_bp)
    return app
    
