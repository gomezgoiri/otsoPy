'''
Created on Jan 1, 2013

@author: tulvur
'''

from abc import abstractmethod, ABCMeta

class TripleSpace(object):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.default_space = "default" # "http://www.morelab.deusto.es"
    
    def join_space(self, space):
        """Joins the *space* identified by an URI."""
        pass
    
    def leave_space(self, space):
        """Leaves a *space* identified by an URI."""
        pass
    
    @abstractmethod
    def get_spaces(self):
        """Get all the spaces joined by this node."""
        pass
    
    @abstractmethod
    def read_uri(self, graph, space=None):
        """
        Reads the graph identified by an *uri* from the *space*.
        @param graph
            The URI which identifies the graph to be returned.
        @param space
            The URI which identifies the space where the graph will be searched.
            If space is 'None' or no value is provided, the default space will be used.
        @throws SpaceNotExistsException
        @return set of triples or 'None' if nothing is found
        """
        pass
    
    @abstractmethod
    def read_template(self, template, space=None):
        """
        Reads a *graph* with a triple which matches a *template* from the *space*.
        This operation is non deterministic.
        @param template
            At least one triple from the returned graph must match this template.
        @param space
            The URI which identifies the space where the graph will be searched.
            If space is 'None' or no value is provided, the default space will be used.
        @throws SpaceNotExistsException
        @return set of triples or 'None' if nothing is found
        """
        pass
    
    @abstractmethod
    def query(self, template, space=None):
        """
        Returns all the triples in the *space* which match the *template*.
        @param template
            All the triples returned must match this template.
        @param space
            The URI which identifies the space where the returned triples belong to.
            If space is 'None' or no value is provided, the default space will be used.
        @throws SpaceNotExistsException
        @return set of triples or 'None' if nothing is found
        """
        pass
    
    @abstractmethod
    def write(self, triples, space=None):
        """
        Writes *triples* in a new graph into the specified *space*.
        @param triples
            Triples which will be written together in a new *graph*
        @param space
            The URI which identifies the space where the triples will be written.
            If space is 'None' or no value is provided, the default space will be used.
        @throws SpaceNotExistsException
        @return The URI which identifies the new graph created.
        """
        pass