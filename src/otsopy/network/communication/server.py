'''
Created on Dec 25, 2012

@author: tulvur
'''
from flask import Flask, request, redirect, render_template
app = Flask(__name__)

class Routes:
    SPACES = '/spaces/'
    SPACE = SPACES + '<path:space>/'
    
    GRAPHS = SPACE + 'graphs/'
    GRAPH = GRAPHS + '<path:graph>/'
    
    _WILDCARDS = 'wildcards/'
    _SUBJECT = '<path:subject>/'
    _PREDICATE = '<path:predicate>/'
    _OBJECT = '<path:obj>/'
    
    GRAPHS_WILCARD = GRAPHS + _WILDCARDS
    GRAPHS_WILCARD_1PARAM = GRAPHS_WILCARD + _SUBJECT
    GRAPHS_WILCARD_2PARAM = GRAPHS_WILCARD_1PARAM + _PREDICATE
    GRAPHS_WILCARD_3PARAM = GRAPHS_WILCARD_2PARAM + _OBJECT
    
    QUERY = SPACE + 'query/'
    QUERY_WILDCARD = QUERY + _WILDCARDS
    QUERY_WILCARD_1PARAM = QUERY_WILDCARD + _SUBJECT
    QUERY_WILCARD_2PARAM = QUERY_WILCARD_1PARAM + _PREDICATE
    QUERY_WILCARD_3PARAM = QUERY_WILCARD_2PARAM + _OBJECT


@app.route('/')
def index():
    return 'Index Page'

@app.route(Routes.SPACES)
def get_spaces():
    """Retrieve the spaces a node is connected to"""
    from otsopy.network.communication.view.spaces import render_spaces
    spaces = app.kernel.get_spaces()
    return render_spaces( spaces )

@app.route(Routes.SPACE)
def get_space(space):
    """"Retrieve a list of the REST services (TSC primitives) which can be consumed on that space.
    The purpose of showing a representation of this resource is to enable browsing.
    
    Also, present the list of graphs written into that space.
    """
    from otsopy.network.communication.view.spaces import render_space
    return render_space( space )

@app.route(Routes.GRAPHS)
def get_graphs(space):
    """Retrieve a list of the graphs written into that space on that node."""
    from otsopy.network.communication.view.graphs import render_graphs
    graphs = app.kernel.get_graph_uris(space)
    return render_graphs( app, space, graphs )

@app.route(Routes.GRAPH)
# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def get_graph(space, graph):
    """read({space},{graph})"""
    #return 'Graph %s in the space %s' % (graph, space)
    from otsopy.network.communication.view.graphs import render_graph
    read_graph = app.kernel.read_uri( graph, space )
    return render_graph( space, graph_id=graph, graph=read_graph )

@app.route(Routes.GRAPHS_WILCARD)
# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def search_graph_by_template(space):
    """Form to perform: read({space},{template})"""
    from otsopy.network.communication.view.wildcards import render_search_by_wildcard
    return render_search_by_wildcard( space )

@app.route(Routes.GRAPHS_WILCARD_1PARAM)
def redirect_read_incomplete_wildcard_1(space, subject):
    return  redirect( request.path + "*/*" )

@app.route(Routes.GRAPHS_WILCARD_2PARAM)
def redirect_read_incomplete_wildcard_2(space, subject, predicate):
    return  redirect( request.path + "*" )

@app.route(Routes.GRAPHS_WILCARD_3PARAM)
# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def get_graph_by_wildcard(space, subject, predicate, obj):
    """read({space},{template})"""
    from otsopy.network.communication.view.wildcards import http_arguments_to_wildcard_template, render_wildcard_graph
    template = http_arguments_to_wildcard_template( subject, predicate, obj )
    #return "let's see: %s" % str(template)
    read_graph = app.kernel.read_template( template, space )
    return render_wildcard_graph( space, read_graph )

@app.route(Routes.QUERY)
def query_pseudo_resource(space):
    """Link to a search form to query."""
    return render_template('query.html', space = space )

@app.route(Routes.QUERY_WILDCARD)
def search_triples_by_template(space):
    """Form to perform: query({space},{template})"""
    from otsopy.network.communication.view.wildcards import render_search_by_wildcard
    return render_search_by_wildcard( space )

@app.route(Routes.QUERY_WILCARD_1PARAM)
def redirect_query_incomplete_wildcard_1(space, subject):
    return  redirect( request.path + "*/*" )

@app.route(Routes.QUERY_WILCARD_2PARAM)
def redirect_query_incomplete_wildcard_2(space, subject, predicate):
    return  redirect( request.path + "*" )

@app.route(Routes.QUERY_WILCARD_3PARAM)
# test: curl -Haccept:text/plain http://localhost:5000/spaces/default/graphs/1
def get_triples_by_wildcard(space, subject, predicate, obj):
    """query({space},{template})"""
    from otsopy.network.communication.view.wildcards import http_arguments_to_wildcard_template
    from otsopy.network.communication.view.query import render_results
    template = http_arguments_to_wildcard_template( subject, predicate, obj )
    triples_result = app.kernel.query( template, space )
    return render_results( triples_result )


if __name__ == '__main__':
    app.debug = True
    app.run()
    #app.run(host='0.0.0.0')