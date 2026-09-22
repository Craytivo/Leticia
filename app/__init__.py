from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY="dev-only-change-me")
    from .routes import main
    app.register_blueprint(main)
    return app
