'''
Methods related with rendering the proper representation.

@author: tulvur
'''

from flask import request


# http://flask.pocoo.org/snippets/45/
def _request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
           request.accept_mimetypes[best] > request.accept_mimetypes['text/html']