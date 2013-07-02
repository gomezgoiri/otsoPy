'''
Created on Dec 18, 2012

@author: tulvur
'''
import unittest
import urllib
import json
import random
from rdflib import URIRef, Graph

from utils.testing import generate_random_graph
from otsopy.impl.centralized import ServerCentralizedKernel


class TestServerCentralizedKernel(unittest.TestCase):
    
    def setUp(self):
        self.kernel = ServerCentralizedKernel()
        self.kernel.app.config['TESTING'] = True
        self.app = self.kernel.app.test_client()

    def tearDown(self):
        pass
    
    def test_index(self):
        rv = self.app.get('/')
        assert 'Index Page' in rv.data
    
    def _get_url(self, url):
        headers = [('Accept', 'application/json')] # to force json
        rv = self.app.get(url, headers=headers)
        return json.loads(rv.data)
    
    # e.g. curl -X GET http://127.0.0.1:5000/spaces/http%3A%2F%2Fwww.morelab.deusto.es -H "Accept: application/json"
    def test_default_space_joined(self):
        response = self._get_url('/spaces')
        assert 'default' in response["spaces"]
        assert len(response["spaces"]) == 1
    
    def test_join_space(self):
        self.kernel.join_space("http://space1");
        response = self._get_url('/spaces')
        assert "http://space1" in response["spaces"]
        assert len(response["spaces"]) == 2
    
    def test_leave_space(self):
        # remove default space
        self.kernel.leave_space('default')
        response = self._get_url('/spaces')
        self.assertFalse( list(response["spaces"]) )
    
    def test_get_graph_uris(self):
        graph_uri = self.kernel.write( generate_random_graph() )
        response = self._get_url('/spaces/%s/graphs' % urllib.quote_plus( self.kernel.data_access._defaultSpace )  )
        assert str(graph_uri) in response["graphs"]


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()