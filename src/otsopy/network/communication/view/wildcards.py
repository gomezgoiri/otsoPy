'''
Created on Jul 2, 2013

@author: tulvur
'''

import urllib
from rdflib import URIRef
from flask import request, redirect, render_template
from otsopy.network.communication.server import Routes


def http_arguments_to_wildcard_template(subject, predicate, obj):
    template = [None, None, None]
    if subject != "*": template[0] = URIRef( urllib.unquote_plus( subject ) )
    if predicate != "*": template[1] = URIRef( urllib.unquote_plus( predicate ) ) 
    if obj != "*": template[2] = URIRef( urllib.unquote_plus( obj ) )
    return tuple(template)

def get_redirection_url_piece_if_needed( arguments ):
    """
    If parameters subject, predicate or object are set, return the appropriate page to redirect.
    Otherwise, return None.
    """
    subj_param = arguments.get('subject')
    pred_param = arguments.get('predicate')
    obj_param = arguments.get('object')
    xsd_type = arguments.get('xsd_type')
    
    if subj_param is not None or pred_param is not None or obj_param is not None:
        # ALREADY QUOTED: subj_param = "*" if subj_param == "" else urllib.quote_plus(subj_param)
        subj_param = "*" if subj_param == "" else urllib.quote_plus(subj_param)
        #if subj_param == "": subj_param = "*"
        #if pred_param == "": pred_param = "*"
        pred_param = "*" if pred_param == "" else urllib.quote_plus(pred_param)
                
        if xsd_type != "none" and obj_param != "":
            return "%s/%s/%s/%s" % ( subj_param, pred_param, xsd_type, obj_param )
        else:
            obj_param = "*" if obj_param == "" else urllib.quote_plus(obj_param)
            #if obj_param == "": obj_param = "*"
            return "%s/%s/%s" % ( subj_param, pred_param, obj_param )            
    #return None # implicit

def render_wildcard_graph( space, read_graph ):
    if read_graph is None:
        # 404
        return "404 Not Found", 404
    else:
        return redirect( str(Routes.GRAPH).replace('<path:space>', space).\
                                            replace('<path:graph>', read_graph.identifier) )

def render_search_by_wildcard( space ):
    redirection_url_piece = get_redirection_url_piece_if_needed( request.args )
    if redirection_url_piece is not None:
        return  redirect( request.path + redirection_url_piece )
    
    html_space = {}
    html_space["name"] = space 
    html_space["url"] = str(Routes.SPACE).replace('<path:space>', space)
    return render_template('wildcard.html', space = html_space )