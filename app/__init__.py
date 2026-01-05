from flask import Flask


def create_app():
    """Application factory"""
    app = Flask(__name__)

    # Register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
