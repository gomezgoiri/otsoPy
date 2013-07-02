'''
Created on Jul 2, 2013

@author: tulvur
'''

from flask import render_template, request


# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def render_results(results):    
    if results is None:
        # 404
        return "404 Not Found", 404
    
    best = request.accept_mimetypes.best_match(['text/n3', 'text/turtle', 'text/plain', 'text/html'])
    
    if best == 'text/html' or request.accept_mimetypes[best] <= request.accept_mimetypes['text/html']: # for  browsers sending */*
        return render_template('query_results.html', results = results.serialize(format="n3") )
    elif best == 'text/n3' :
        # 'xml', 'n3', 'turtle', 'nt', 'pretty-xml', trix' are built in.
        return results.serialize(format="n3")
    elif best == 'text/turtle':
        return results.serialize(format="turtle")
    elif best == 'text/plain':
        return results.serialize(format="nt")
    
    # Else:
    return "406 Not Acceptable", 406