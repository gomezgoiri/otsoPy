'''
Created on Dec 25, 2012

@author: tulvur
'''

import urllib
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

# http://flask.pocoo.org/snippets/45/
def request_wants_json():
    best = request.accept_mimetypes.best_match(['application/json', 'text/html'])
    return best == 'application/json' and \
           request.accept_mimetypes[best] > request.accept_mimetypes['text/html']

@app.route('/')
def index():
    return 'Index Page'

@app.route('/spaces')
def get_spaces():
    """Retrieve the spaces a node is connected to"""
    #return 'Hello World'
    spaces = app.kernel.get_spaces()
    if request_wants_json():
        return jsonify( spaces = spaces )
    
    html_spaces = []
    for space in spaces:
        element = {}
        element['name'] = space
        element['url'] = "spaces/%s" % urllib.quote_plus(space) 
        html_spaces.append( element )
    return render_template('spaces.html', spaces = html_spaces )

@app.route('/spaces/<path:space>')
def get_space(space):
    """"Retrieve a list of the REST services (TSC primitives) which can be consumed on that space.
    The purpose of showing a representation of this resource is to enable browsing.
    
    Also, present the list of graphs written into that space.
    """
    space_dict = {}
    space_dict['name'] = space
    space_escaped = urllib.quote_plus(space)
    space_dict['resources'] = []
    
    element = {}
    element['name'] = "graphs/"
    element['url'] = "%s/graphs" % space_escaped
    space_dict['resources'].append(element)
    
    element = {}
    element['name'] = "query/"
    element['url'] = "%s/query" % space_escaped
    space_dict['resources'].append(element)    
    
    if request_wants_json():
        return jsonify( space = space_dict )
    
    return render_template('space.html', space = space_dict )

@app.route('/spaces/<path:space>/graphs')
def get_graphs(space):
    """Retrieve a list of the graphs written into that space on that node."""
    graphs = app.kernel.get_graph_uris(space)
    if request_wants_json():
        return jsonify( graphs = graphs )
    
    html_graphs = []
    for graph in graphs:
        element = {}
        element['name'] = graph
        element['url'] = "/spaces/%s/graphs/%s" % (urllib.quote_plus(space), urllib.quote_plus(graph)) 
        html_graphs.append( element )
    #print graphs
    return render_template('graphs.html', space = space, graphs = html_graphs )

@app.route('/spaces/<path:space>/graphs/<path:graph>')
# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def get_graph(space, graph):
    """read({space},{graph})"""
    #return 'Graph %s in the space %s' % (graph, space)
    read_graph = app.kernel.read_uri( graph, space )
    
    if read_graph is None:
        # 404
        return "404 Not Found", 404
    else:
        best = request.accept_mimetypes.best_match(['text/n3', 'text/turtle', 'text/plain', 'text/html'])
        
        if best == 'text/html' or request.accept_mimetypes[best] <= request.accept_mimetypes['text/html']: # for  browsers sending */*
            html_space = {}
            html_space["name"] = space
            html_space["url"] = "/spaces/%s"%space
            
            html_graph = {}
            html_graph["name"] = graph
            html_graph["content"] = read_graph.serialize(format="n3")
            
            return render_template('graph.html', space = html_space, graph = html_graph )
        elif best == 'text/n3' :
            # 'xml', 'n3', 'turtle', 'nt', 'pretty-xml', trix' are built in.
            return read_graph.serialize(format="n3")
        elif best == 'text/turtle':
            return read_graph.serialize(format="turtle")
        elif best == 'text/plain':
            return read_graph.serialize(format="nt")
        else:
            return "406 Not Acceptable", 406
    
if __name__ == '__main__':
    app.debug = True
    app.run()
    #app.run(host='0.0.0.0')