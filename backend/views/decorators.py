from flask import g, request, jsonify
from mongoengine import DoesNotExist
from functools import wraps
import logging

from backend.services.auth import AuthTokenLoadService


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return jsonify({'message': 'token required'}), 401

        try:
            auth_token = AuthTokenLoadService.get_auth_token(token)

        except DoesNotExist:
            return jsonify({'message': 'not authenticated'}), 401

        kwargs['auth_token'] = auth_token
        g.user = auth_token.user
        return func(*args, **kwargs)

    return wrapper


def handle_internal_server_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except RuntimeError as e:
            logging.debug(e)
            return jsonify({'message': 'Internal Server Error'}), 500

    return wrapper
