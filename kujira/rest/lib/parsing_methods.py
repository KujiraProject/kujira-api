"""Library which contains helpers used in JSON API parsing process.
Helpers defined:
- parse_and_return - for parsing response to JSON API format
                using method defined in appropriate controller
- create_error_422 - creating error 422 packed to JSON API format"""

import json

from flask import Response


def parse_and_return(method, response):
    """Method which is parsing response using appropriate method and creates JSON Response"""
    json_response = json.dumps(response)
    json_dict = json.loads(json_response)
    output = method(json_dict)
    json_output = Response(json.dumps(output, indent=2),
                           content_type='application/json')
    return json_output


def create_error_422(source, message):
    """Method which creates error with StatusCode 422 and creates JSON Response with it"""
    errors = {'errors': [{'status': '422'}]}
    errors['errors'][0]['source'] = str(source)
    errors['errors'][0]['details'] = message
    json_errors = Response(json.dumps(errors, indent=2),
                           content_type="application/vnd.api+json",
                           status=422)
    return json_errors


def parse_cluster_pool(type_name, content_dict):
    """Function which restructures cluster's dict entries into appropriate categories"""
    result = {
        'type': type_name
    }
    attributes = {}
    for key, value in content_dict.iteritems():
        key = key.replace('_', '-')
        if str(key) == 'id':
            result['id'] = str(value)
        attributes[str(key)] = value
    result['attributes'] = attributes
    return result
