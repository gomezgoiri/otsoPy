'''
Created on Dec 25, 2012

@author: tulvur
'''

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/spaces')
def get_spaces():
    """Retrieve the spaces a node is connected to"""
    return 'Hello World'

@app.route('/spaces/<path:space>')
def get_space(space):
    """"Retrieve a list of the REST services (TSC primitives) which can be consumed on that space.
    The purpose of showing a representation of this resource is to enable browsing."""
    return 'Space %s' % space

@app.route('/spaces/<path:space>/graphs')
def get_graphs(space):
    """Retrieve a list of the graphs written into that space on that node."""
    return 'Graphs for the space %s' % space

@app.route('/spaces/<path:space>/graphs/<path:graph>')
def get_graph(space, graph):
    """read({space},{graph})"""
    return 'Graph %s in the space %s' % (graph, space)

if __name__ == '__main__':
    app.debug = True
    app.run()
    #app.run(host='0.0.0.0')