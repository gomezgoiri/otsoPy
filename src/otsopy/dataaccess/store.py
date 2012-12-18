import threading
import random

from copy import deepcopy
from rdflib import ConjunctiveGraph, URIRef, Graph

from otsopy.dataaccess.util import locked


class DataAccess(object):
    def __init__(self, defaultSpace="http://www.morelab.deusto.es"):
        self.stores = {}
        self.__defaultSpace = defaultSpace
        if defaultSpace is not None:
            self.stores[defaultSpace] = Store() # join not implemented yet
    
    def getSpace(self, space):
        if space == None:
            space = self.__defaultSpace
        if not self.stores.has_key(space):
            raise Exception("Space '%s' does not exist." % space)
        return self.stores[space]
    
    def write(self, triples, space=None):
        store = self.getSpace(space)
        return store.write(triples)
        
    def read_uri(self, uri, space=None):
        store = self.getSpace(space)
        return store.read_uri(uri)
    
    def read_wildcard(self, subject, predicate, obj, space=None):
        store = self.getSpace(space)
        return store.read_wildcard(subject, predicate, obj)
    
    def take_uri(self, uri, space=None):
        store = self.getSpace(space)
        return store.take_uri(uri)
    
    def take_wildcard(self, subject, predicate, obj, space=None):
        store = self.getSpace(space)
        return store.take_wildcard(subject, predicate, obj)
    
    def query_wildcard(self, subject, predicate, obj, space=None):
        store = self.getSpace(space)
        return store.query_wildcard(subject, predicate, obj)


class Store(object):
    def __init__(self):
        self.graphs = ConjunctiveGraph(store='default')
        self._lock = threading.RLock()

    @locked
    def _print(self):
        print "Graph %r" % self.graphs                

    def __write_graph(self, graph):
        self._lock.acquire()
        while True:
            new_uri = URIRef('http://otsopack/%s' % random.randint(0, 1000))
            if new_uri in filter(lambda n: n.identifier!=new_uri, self.graphs.contexts()):
                continue
            
            gr = Graph(self.graphs.store, URIRef(new_uri))
            gr += graph
            return new_uri
    
    @locked
    def write(self, triples):        
        if not isinstance(triples, Graph):
            raise Exception("'triples' must be a Graph.")

        new_uri = self.__write_graph(triples)
        self._lock.release()
        return new_uri

    @locked
    def read_uri(self, uri):
        ret = Graph(self.graphs.store, URIRef(uri))
        return deepcopy(ret) if ret else None

    @locked
    def read_wildcard(self, subject, predicate, obj):
        gr = self._find_graph(subject, predicate, obj)
        return deepcopy(gr)

    @locked
    def take_uri(self, uri):
        try:
            context = URIRef(uri)
            ret = Graph(self.graphs.store, context)
            self.graphs.remove_context(context)
        except KeyError:
            return None
        return deepcopy(ret) if ret else None

    @locked
    def take_wildcard(self, subject, predicate, obj):
        try:
            ret = self._find_graph(subject, predicate, obj)
            self.graphs.remove_context(ret.identifier)
        except KeyError:
            return None
        return ret
    
    @locked
    def query_wildcard(self, subject, predicate, obj):
        ret = Graph()
        for t in self.graphs.triples((subject, predicate, obj)):
            ret.add(t)
        return ret if len(ret)>0 else None

    def _find_graph(self, subject, predicate, obj):
        for graph in self.graphs.contexts(): #(subject, predicate, obj)):
            for t in graph.triples((subject, predicate, obj)):
                return graph # if it has at least a triple matching that triple, we return the graph
        return None