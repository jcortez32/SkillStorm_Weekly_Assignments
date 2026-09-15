from flask import Flask
from .routes import main_bp, ops_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(ops_bp)
    return app