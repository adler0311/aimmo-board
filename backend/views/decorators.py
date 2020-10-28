from backend.services.auth_service import AuthService
from flask import request, jsonify
from mongoengine import DoesNotExist
from functools import wraps
import logging

auth_service = AuthService()


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return jsonify({'message': 'token required'}), 401

        try:
            auth_token = auth_service.get_auth_token(token)

        except DoesNotExist:
            return jsonify({'message': 'not authenticated'}), 401

        kwargs['auth_token'] = auth_token
        return func(*args, **kwargs)

    return wrapper


def handle_internal_server_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.debug(e)
            return jsonify({'message': 'Internal Server Error'}), 500

    return wrapper