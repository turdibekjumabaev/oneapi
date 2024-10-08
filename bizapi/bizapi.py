from .types import Request, Response
from .router import Router
from .errors import page_not_found, method_not_allowed

import inspect


class BizAPI:

    def __init__(self):
        self.router = Router()

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()
        handler_data, kwargs = self.router.find_handler(request)
        if handler_data is not None:
            handler = handler_data.get(request.method, None)

            if handler is None:
                return method_not_allowed(response)

            if inspect.isclass(handler):
                handler_method = getattr(handler, request.method.lower(), None)
                if handler_method is None:
                    return method_not_allowed(response)
                handler_method(request, response, **kwargs)
            else:
                handler(request, response, **kwargs)
        else:
            return page_not_found(response)
        return response

    def route(self, path: str, methods: list = None):
        if methods is None:
            methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH', 'TRACE', 'CONNECT']

        def wrapper(func):
            self.router.add_route(path, func, methods)
            return func

        return wrapper

    def add_method_route(self, path: str, methods: list = None):
        def wrapper(func):
            self.router.add_route(path, func, methods)
            return func

        return wrapper

    def get(self, path: str):
        return self.add_method_route(path, ['GET'])

    def post(self, path: str):
        return self.add_method_route(path, ['POST'])

    def put(self, path: str):
        return self.add_method_route(path, ['PUT'])

    def patch(self, path: str):
        return self.add_method_route(path, ['PATCH'])

    def delete(self, path: str):
        return self.add_method_route(path, ['DELETE'])

    def head(self, path: str):
        return self.add_method_route(path, ['HEAD'])

    def options(self, path: str):
        return self.add_method_route(path, ['OPTIONS'])

    def trace(self, path: str):
        return self.add_method_route(path, ['TRACE'])

    def connect(self, path: str):
        return self.add_method_route(path, ['CONNECT'])
