"""
Triple space implementation which manages the space in a single node (centralized).
"""
from otsopy.triplespace import TripleSpace
from otsopy.dataaccess.store import DataAccess

class ServerCentralizedKernel(TripleSpace):
    """
    Server side of the centralized Triple Space implementation.
    """
    
    def __init__(self):
        super(ServerCentralizedKernel, self).__init__()
        self.data_access = DataAccess() 
        self._create_server()
        
    def _create_server(self):
        from otsopy.network.communication.server import app
        self.app = app
        self.app.kernel = self
    
    def join_space(self, space):
        self.data_access.join_space(space)
    
    def leave_space(self, space):
        self.data_access.leave_space(space)
    
    def get_spaces(self):
        return self.data_access.get_spaces()
    
    def get_graph_uris(self, space):
        return self.data_access.get_graph_uris(space)
    
    def read_uri(self, graph, space=None):
        return self.data_access.read_uri(graph, space=space)
    
    def read_template(self, template, space=None):
        return self.data_access.read_wildcard(*template, space=space)
    
    def query(self, template, space=None):
        return self.data_access.query_wildcard(*template, space=space)
    
    def write(self, triples, space=None):
        return self.data_access.write(triples, space=space)

class ClientCentralizedKernel(TripleSpace):
    """
    Server side of the centralized Triple Space implementation.
    """
    
    def __init__(self):
        super(ClientCentralizedKernel, self).__init__()
    
    def join_space(self, space):
        pass
    
    def leave_space(self, space):
        pass
    
    def get_spaces(self):
        pass
    
    def read_uri(self, graph, space=None):
        pass
    
    def read_template(self, template, space=None):
        pass
    
    def query(self, template, space=None):
        pass
    
    def write(self, triples, space=None):
        pass

if __name__ == '__main__':
    sc = ServerCentralizedKernel()
    
    from utils.testing import generate_random_graph
    sc.write( generate_random_graph() )
    
    sc.app.debug = True
    sc.app.run()
    #app.run(host='0.0.0.0')