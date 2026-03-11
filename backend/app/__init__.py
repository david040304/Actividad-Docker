from flask import Flask
from flask_cors import CORS

from config import Config
from app.database import init_db, close_db


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config())

    # Permitir peticiones desde el frontend (Nginx en otro contenedor)
    CORS(app)

    # Base de datos
    init_db(app)
    app.teardown_appcontext(close_db)

    # Registrar blueprints
    from app.routes.contacts import contacts_bp
    from app.routes.validator import validator_bp
    from app.routes.health import health_bp

    app.register_blueprint(contacts_bp)
    app.register_blueprint(validator_bp)
    app.register_blueprint(health_bp)

    return app
