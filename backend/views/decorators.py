from flask import request, jsonify
from backend.models.auth_token import AuthToken
from mongoengine import DoesNotExist
from functools import wraps
import logging


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token is None:
            return jsonify({'message': 'token required'}), 401

        try:
            auth_token = AuthToken.objects.get(token=token)

        except DoesNotExist as e:
            return jsonify({'message': 'not authenticated'}), 401

        kwargs['auth_token'] = auth_token
        return func(*args, **kwargs)

    return wrapper


def input_data_required(func):
    def wrapper(*args, **kwargs):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'message': 'No input data provided'}), 400

        kwargs['json_data'] = json_data
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
