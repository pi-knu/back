import os
from flask import Flask
from flask_cors import CORS

from controllers.users import bp as users_bp
from controllers.lots import bp as lots_bp
from controllers.health import bp as health_bp


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    CORS(app, resources={r"/*": {"origins": "*"}})

    app.register_blueprint(users_bp)
    app.register_blueprint(lots_bp)
    app.register_blueprint(health_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT")))