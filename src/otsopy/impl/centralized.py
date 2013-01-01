"""
Triple space implementation which manages the space in a single node (centralized).
"""
from otsopy.triplespace import TripleSpace

class ServerCentralizedKernel(TripleSpace):
    """
    Server side of the centralized Triple Space implementation.
    """
    
    def __init__(self):
        super(ServerCentralizedKernel, self).__init__()
    
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