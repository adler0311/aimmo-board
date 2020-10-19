from flask import request, jsonify
from backend.models.auth_token import AuthToken
from mongoengine import DoesNotExist


def token_required(func):
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
