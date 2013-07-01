'''
Created on Jul 1, 2013

@author: tulvur
'''

import random
from rdflib import URIRef, Graph
    
# todo encapsulate and avoid repetition!
def generate_random_URI():
    domains = ("www.deusto.es", "www.morelab.deusto.es", "aitor.gomezgoiri.net")
    return URIRef( "http://%s/%d"%(random.choice(domains), random.randint(0, 1000)) )

def generate_random_triple():
    return ( generate_random_URI(), generate_random_URI(), generate_random_URI() )

def generate_random_graph():
    graph = Graph()
    for _ in range(10):
        graph.add( generate_random_triple() )
    return graph