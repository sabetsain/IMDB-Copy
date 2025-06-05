import os
from . import db, routes
from flask import Flask
from flask_cors import CORS


def create_app():
    """
    Description
    -----------
    This function creates and configures the Flask application instance.

    Parameters
    ----------
    None
    
    Returns
    -------
    app : Flask
        The configured Flask application instance.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.psql'),
    )

    CORS(app, 
         origins=["http://localhost:5173", "http://127.0.0.1:5173"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"],
         supports_credentials=True
    )
    
    db.init_app(app)
    app.register_blueprint(routes.bp)

    return app