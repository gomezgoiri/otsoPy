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
    return render_template('spaces.html', spaces = spaces )

def render_space(space):    
    if _request_wants_json():
        space_dict = {}
        space_dict['name'] = space
        space_escaped = urllib.quote_plus(space)
        space_dict['resources'] = []
        
        element = {}
        element['name'] = "query/"
        element['url'] = "%s/query" % space_escaped
        space_dict['resources'].append(element)
        
        return jsonify( space = space_dict )
    
    return render_template('space.html', space = space, resources = ["graphs", "query"] )