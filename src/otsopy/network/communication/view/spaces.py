'''
Created on Jul 2, 2013

@author: tulvur
'''

import urllib
from flask import jsonify, render_template
from otsopy.network.communication.view.utils import _request_wants_json


def render_spaces(spaces):
    if _request_wants_json():
        return jsonify( spaces = spaces )
    
    html_spaces = []
    for space in spaces:
        element = {}
        element['name'] = space
        element['url'] = "spaces/%s" % urllib.quote_plus(space)
        html_spaces.append( element )
    return render_template('spaces.html', spaces = html_spaces )

def render_space(space):
    space_dict = {}
    space_dict['name'] = space
    space_escaped = urllib.quote_plus(space)
    space_dict['resources'] = []
    
    element = {}
    element['name'] = "graphs/"
    element['url'] = "%s/graphs" % space_escaped
    space_dict['resources'].append(element)
    
    element = {}
    element['name'] = "query/"
    element['url'] = "%s/query" % space_escaped
    space_dict['resources'].append(element)    
    
    if _request_wants_json():
        return jsonify( space = space_dict )
    
    return render_template('space.html', space = space_dict )