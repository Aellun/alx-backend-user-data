#!/usr/bin/env python3
"""
Route module for the API.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)

# CORS config to allow requests
# from any origin for the API routes
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize authentication based
# on the AUTH_TYPE environment variable
auth = None
AUTH_TYPE = getenv("AUTH_TYPE")

# Check the AUTH_TYPE and initialize the
# corresponding authentication class
if AUTH_TYPE == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.before_request
def before_request():
    """
    Before request handler to enforce authentication rules.
    """
    if auth is None:
        return

    excluded_list = ['/api/v1/status/',
                     '/api/v1/unauthorized/',
                     '/api/v1/forbidden/'
                     ]

    if auth.require_auth(request.path, excluded_list):
        if auth.authorization_header(request) is None:
            abort(401, description="Unauthorized")
        if auth.current_user(request) is None:
            abort(403, description='Forbidden')


@app.errorhandler(404)
def not_found(error) -> str:
    """
    Not found handler.
    return:
        jsonify({"error": "Not found"}), 404
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
