'''
Created on Dec 18, 2012

@author: tulvur
'''
import unittest
import random
from rdflib import URIRef, Graph
from otsopy.dataaccess.store import Store

class TestStore(unittest.TestCase):

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
        for tripls in self.triples:
            graph = Graph()
            for t in tripls:
                graph.add(t)
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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()