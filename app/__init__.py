from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from .config import Config
from .models import db
import logging
import warnings

warnings.filterwarnings('ignore', message='.*Textual SQL expression.*')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    # Logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[logging.StreamHandler()]
    )

    # Register blueprints
    from .auth import auth_bp
    from .inspection import inspection_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(inspection_bp)

    @app.before_request
    def log_request():
        import flask
        logging.info(f"{flask.request.method} {flask.request.path}")

    # Global error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error(f"Unhandled Exception: {e}")
        return jsonify({'error': 'an unexpected error occured.'}), 500

    return app