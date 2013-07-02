'''
Created on Jul 2, 2013

@author: tulvur
'''

import urllib
from flask import jsonify, render_template, request
from otsopy.network.communication.server import Routes
from otsopy.network.communication.view.utils import _request_wants_json


def render_graphs(app, space, graphs):
    if _request_wants_json():
        return jsonify( graphs = graphs )

    html_graphs = []
    for graph in graphs:
        element = {}
        element['name'] = graph
        element['url'] = str(Routes.GRAPH).\
                            replace('<path:space>', urllib.quote_plus(space)).\
                            replace('<path:graph>', urllib.quote_plus(graph))
        html_graphs.append( element )
    #print graphs
    return render_template('graphs.html', space = space, graphs = html_graphs )


# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def render_graph(space, graph_id, graph):    
    if graph is None:
        # 404
        return "404 Not Found", 404
    
    best = request.accept_mimetypes.best_match(['text/n3', 'text/turtle', 'text/plain', 'text/html'])
    
    if best == 'text/html' or request.accept_mimetypes[best] <= request.accept_mimetypes['text/html']: # for  browsers sending */*
        html_space = {}
        html_space["name"] = space
        html_space["url"] = str(Routes.SPACE).replace('<path:space>', space)
        
        html_graph = {}
        html_graph["name"] = graph_id
        html_graph["content"] = graph.serialize(format="n3")
        
        return render_template('graph.html', space = html_space, graph = html_graph )
    elif best == 'text/n3' :
        # 'xml', 'n3', 'turtle', 'nt', 'pretty-xml', trix' are built in.
        return graph.serialize(format="n3")
    elif best == 'text/turtle':
        return graph.serialize(format="turtle")
    elif best == 'text/plain':
        return graph.serialize(format="nt")
    
    # Else:
    return "406 Not Acceptable", 406