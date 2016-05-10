import json

from flask import Response


"""Library which contains helpers used in JSON API parsing process.
Helpers defined:
- parse_and_return - for parsing response to JSON API format using method defined in appropriate controller
- create_error_422 - creating error 422 packed to JSON API format"""


def parse_and_return(method, response):
    json_response = json.dumps(response)
    json_dict = json.loads(json_response)
    output = method(json_dict)
    json_output = Response(json.dumps(output, indent=2), content_type='application/json')
    return json_output


def create_error_422(source, message):
    errors = {'errors': [{'status': '422'}]}
    errors['errors'][0]['source'] = str(source)
    errors['errors'][0]['details'] = message
    json_errors = Response(json.dumps(errors, indent=2), content_type="application/vnd.api+json", status=422)
    return json_errors