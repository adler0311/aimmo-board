from flask import g, request, jsonify
from mongoengine import DoesNotExist
from functools import wraps
import logging

from backend.errors import ApiError, ForbiddenError
from backend.models.auth_token import AuthToken


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return jsonify({'message': 'token required'}), 401

        try:
            auth_token = AuthToken.objects.get(token=token)

        except DoesNotExist:
            return jsonify({'message': 'not authenticated'}), 401

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


def handle_not_found_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DoesNotExist:
            raise ApiError(status_code=404)

    return wrapper


def handle_forbidden_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ForbiddenError as e:
            raise ApiError(message=e.message, status_code=403)

    return wrapper
