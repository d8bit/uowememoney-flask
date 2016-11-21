from flask import session, abort

class Middleware(object):
    # Simple WSGI middleware
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        url = environ['PATH_INFO']
        # if "login" in url or self.app.userLoggedIn():
        return self.app(environ, start_response)
        abort(401)
