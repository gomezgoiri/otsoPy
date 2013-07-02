'''
Created on Dec 25, 2012

@author: tulvur
'''
from flask import Flask, request, redirect
app = Flask(__name__)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/spaces')
def get_spaces():
    """Retrieve the spaces a node is connected to"""
    from otsopy.network.communication.view.spaces import render_spaces
    spaces = app.kernel.get_spaces()
    return render_spaces( spaces )

@app.route('/spaces/<path:space>')
def get_space(space):
    """"Retrieve a list of the REST services (TSC primitives) which can be consumed on that space.
    The purpose of showing a representation of this resource is to enable browsing.
    
    Also, present the list of graphs written into that space.
    """
    from otsopy.network.communication.view.spaces import render_space
    return render_space( space )

@app.route('/spaces/<path:space>/graphs')
def get_graphs(space):
    """Retrieve a list of the graphs written into that space on that node."""
    from otsopy.network.communication.view.graphs import render_graphs
    graphs = app.kernel.get_graph_uris(space)
    return render_graphs( app, space, graphs )

@app.route('/spaces/<path:space>/graphs/<path:graph>')
# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def get_graph(space, graph):
    """read({space},{graph})"""
    #return 'Graph %s in the space %s' % (graph, space)
    from otsopy.network.communication.view.graphs import render_graph
    read_graph = app.kernel.read_uri( graph, space )
    return render_graph( space, graph_id=graph, graph=read_graph )

@app.route('/spaces/<path:space>/graphs/wildcards')
# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def search_graph_by_template(space):
    """Retrieve a list of the graphs written into that space on that node."""
    from otsopy.network.communication.view.wildcards import render_search_by_wildcard
    return render_search_by_wildcard( space )

@app.route('/spaces/<path:space>/graphs/wildcards/<path:subject>')
def redirect_incomplete_wildcard_1(space, subject):
    return  redirect( request.path + "/*/*" )

@app.route('/spaces/<path:space>/graphs/wildcards/<path:subject>/<path:predicate>')
def redirect_incomplete_wildcard_2(space, subject, predicate):
    return  redirect( request.path + "/*" )

@app.route('/spaces/<path:space>/graphs/wildcards/<path:subject>/<path:predicate>/<path:obj>')
# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def get_graph_by_wildcard(space, subject, predicate, obj):
    """read({template},{graph})"""
    from otsopy.network.communication.view.wildcards import http_arguments_to_wildcard_template, render_wildcard_graph
    template = http_arguments_to_wildcard_template( subject, predicate, obj )
    #return "let's see: %s" % template
    read_graph = app.kernel.read_template( template, space )
    return render_wildcard_graph( space, read_graph )

    
if __name__ == '__main__':
    app.debug = True
    app.run()
    #app.run(host='0.0.0.0')