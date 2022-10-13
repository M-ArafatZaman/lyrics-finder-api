from flask import request
from functools import wraps

# Create a middleware for adding CORS header parameters to returning requests
def enableCORS(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before calling
        #         
        response = func(*args, **kwargs)

        # After calling
        response.headers["Access-Control-Allow-Origin"] = "*"

        return response

    return wrapper