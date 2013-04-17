'''
Created on Dec 18, 2012

@author: tulvur
'''
import unittest
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
    
    def test_not_spaces_joined(self):
        rv = self.app.get('/spaces')
        assert 'Hello World' in rv.data

    def test_join_space(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()