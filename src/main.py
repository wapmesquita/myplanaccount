import webapp2
import logging
import os
from handler.http_handler import ServiceRouter, AuthorizationRouter, GacRouter

app = webapp2.WSGIApplication([('/s/.*', ServiceRouter), ('/g/.*', GacRouter),('/docs-authorization.*', AuthorizationRouter)], debug=True)

def main():
    logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    main()
