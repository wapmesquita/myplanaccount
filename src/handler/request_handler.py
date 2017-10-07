import webapp2
from util import json_util

def json(fnc):
    def inner(*args, **kwargs):
        response = args[0].response
        response.status = 200
        response.headers['Content-Type'] = 'application/json'
        from_func = fnc(*args, **kwargs)

        result = None
        if not from_func:
            result = {}

        elif isinstance(from_func, dict):
            result = json_util.from_json(from_func)
        elif isinstance(from_func, list):
            if len(from_func) > 0:
                if hasattr(from_func[0], 'to_json'):
                    from_func = {'result': [obj.to_json() for obj in from_func]}
                result = json_util.from_json(from_func)
        elif isinstance(from_func, ModelBase):
            result = from_func.to_json()
            result = json_util.from_json(result)
        return response.out.write(result)

    return inner

class Request(webapp2.RequestHandler):

    def read_json(self):
        return json_util.to_json(self.request.body)

    def forbidden(self):
        self.response.status = 403

    def param(self, key):
        value = None
        if key in self.request.GET:
            value = self.request.GET[key]
        if isinstance(value, unicode):
            value = value.encode('UTF-8')
            return value
        return None

    def param_long(self, key):
        value = self.param(key)
        if value:
            return long(value)
        return None

    def param_boolean(self, key):
        value = self.param(key)
        if value:
            return value.upper() == 'TRUE'
        return None
