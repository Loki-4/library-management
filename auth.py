import functools
from flask import request, jsonify

def token_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({"message": "Token is missing"}), 403
        if token != 'your-secret-token':
            return jsonify({"message": "Invalid token"}), 403
        return f(*args, **kwargs)
    return decorated_function
