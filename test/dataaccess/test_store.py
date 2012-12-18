'''
Created on Dec 18, 2012

@author: tulvur
'''
import unittest
import random

from copy import deepcopy
from rdflib import URIRef, Graph
from otsopy.dataaccess.store import Store

RECOGNIZABLE_SUBJECT ="http://subject_%d"
RECOGNIZABLE_PREDICATE = "http://predicate_%d"
RECOGNIZABLE_OBJECT =  "http://object_%d"

class TestStore(unittest.TestCase):

    def generate_recognizable_triple(self, id):
        return ( URIRef( RECOGNIZABLE_SUBJECT%(id) ),
                 URIRef( RECOGNIZABLE_PREDICATE%(id) ),
                 URIRef( RECOGNIZABLE_OBJECT%(id) ) ) 

    def generate_random_URI(self):
        domains = ("www.deusto.es", "www.morelab.deusto.es", "aitor.gomezgoiri.net")
        return URIRef( "http://%s/%d"%(random.choice(domains), random.randint(0, 1000)) )

    def generate_random_triple(self):
        return (self.generate_random_URI(), self.generate_random_URI(), self.generate_random_URI())

    def setUp(self):
        self.triples = []
        
        self.triples.append( [self.generate_random_triple() for _ in range(10)] )
        self.triples.append( [self.generate_random_triple() for _ in range(10)] )
        self.triples.append( [self.generate_random_triple() for _ in range(10)] )
        
        self.graphs = []
        i = 0
        for tripls in self.triples:
            graph = Graph()
            for t in tripls:
                graph.add(t)
            graph.add( self.generate_recognizable_triple(i) )
            i += 1
            self.graphs.append(graph)
        
        self.store = Store()


    def tearDown(self):
        pass

    def assertItemsIsomorphic(self, expected_graphs, test_graphs):
        self.assertEquals( len(expected_graphs), len(test_graphs) )
        
        for g in test_graphs:
            found = False
            for expected in expected_graphs:
                if g.isomorphic(expected):
                    found = True
                    expected_graphs.remove(expected)
                    break
            if not found:
                self.fail("Graph '%s' not expected."%(g.identifier))
        # everything OK

    def test_write(self):
        self.assertFalse( list(self.store.graphs.contexts()) )
        
        self.store.write(self.graphs[0])
        contexts = list(self.store.graphs.contexts())
        self.assertEquals(1, len(contexts))
        self.assertItemsIsomorphic( [self.graphs[0],], contexts)
        
        self.store.write(self.graphs[2])
        contexts = list(self.store.graphs.contexts())
        self.assertEquals(2, len(contexts))
        self.assertItemsIsomorphic( [self.graphs[0], self.graphs[2],], contexts)
    
    def test_read_uri(self):
        uris = []
        uris.append( self.store.write(self.graphs[0]) )
        uris.append( self.store.write(self.graphs[1]) )
        uris.append( self.store.write(self.graphs[2]) )
        
        for uri, expected in zip(uris, self.graphs):
            graph = self.store.read_uri(uri)
            self.assertTrue( graph.isomorphic(expected) )
            
    def test_read_wildcard(self):
        self.store.write(self.graphs[0])
        self.store.write(self.graphs[1])
        self.store.write(self.graphs[2])
        
        i = 0
        for expected in self.graphs:
            graph = self.store.read_wildcard( URIRef(RECOGNIZABLE_SUBJECT%(i)), None, None )
            self.assertTrue( graph.isomorphic(expected) )
            
            graph = self.store.read_wildcard( None, URIRef(RECOGNIZABLE_PREDICATE%(i)), None )
            self.assertTrue( graph.isomorphic(expected) )
            
            graph = self.store.read_wildcard( None, None, URIRef(RECOGNIZABLE_OBJECT%(i)) )
            self.assertTrue( graph.isomorphic(expected) )
            
            # TODO try other combinations?
            
            i += 1
        
    def test_take_uri(self):
        uris = []
        uris.append( self.store.write(self.graphs[0]) )
        uris.append( self.store.write(self.graphs[1]) )
        uris.append( self.store.write(self.graphs[2]) )
        
        for uri, expected in zip(uris, self.graphs):
            graph = self.store.take_uri(uri)
            self.assertTrue( graph.isomorphic(expected) )
            
            # the second time is not there anymore
            graph = self.store.take_uri(uri)
            self.assertEquals( None, graph )        
    
    def assert_takes_wildcard(self, expected_graph, *wildcard):
        # only valid for wildcards with just match with a graph inside the space
        graph = self.store.take_wildcard( *wildcard )
        self.assertTrue( graph.isomorphic(expected_graph) )
        
        # the second time is not there anymore
        graph = self.store.take_wildcard( *wildcard )
        self.assertEquals( None, graph )
    
    def test_take_wildcard(self):
        self.store.write(self.graphs[0])
        self.store.write(self.graphs[1])
        self.store.write(self.graphs[2])
        
        self.assert_takes_wildcard( self.graphs[0], URIRef(RECOGNIZABLE_SUBJECT%(0)), None, None )        
        self.assert_takes_wildcard( self.graphs[1], None, URIRef(RECOGNIZABLE_PREDICATE%(1)), None )
        self.assert_takes_wildcard( self.graphs[2], None, None, URIRef(RECOGNIZABLE_OBJECT%(2)) )
            
        # TODO try other combinations
        # TODO try with 2 or more graphs matching a template


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()