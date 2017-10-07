import importlib, request_handler
from gac import flow_utils, constants, oauth_checker

class AuthorizationRouter(request_handler.Request):

    def dispatch(self):
        req = self.request
        resp = self.response
        checker = oauth_checker.OAuthChecker(req, resp)
        self.redirect(checker.createCookie())

class GacRouter(request_handler.Request):

    def dispatch(self):
        req = self.request
        resp = self.response
        checker = oauth_checker.OAuthChecker(req, resp)
        if not checker.verify():
            checker.getAuthURI()
        else:
            obj = _get_obj(self)
            method = getattr(obj, self.request.method.lower())
            method()

class ServiceRouter(request_handler.Request):

    def dispatch(self):
        obj = _get_obj(self)
        method = getattr(obj, self.request.method.lower())
        method()


def _get_obj(that):
    path = that.request.path
    req = that.request
    resp = that.response
    print path
    entire_path = path.split('/')
    module = entire_path[2]
    clazz = entire_path[3]
    m = importlib.import_module('service.' + module)
    clazz_name = clazz.split('?')[0]
    print clazz_name
    clazz = getattr(m, clazz_name + "Service")
    return clazz(req, resp)
