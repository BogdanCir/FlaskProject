from flask import Flask
from flask_cors import CORS
from app.db import db_session

def create_app(testing=False):
    app = Flask(__name__)
    CORS(app)

    if testing:
        app.config["TESTING"] = True

    from app.api.routes import bp
    app.register_blueprint(bp)

    # inchidem sesiunea db
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
