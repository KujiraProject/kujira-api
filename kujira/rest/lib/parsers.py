import json

from flask import Response


def json_api_parser(response):
    json_response = json.dumps(response)
    json_dict = json.loads(json_response)
    data = dict_iterate(json_dict)
    return data


def dict_iterate(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        print e.message
    data = {'data': {}}
    attributes = {}
    if new_dict:
        for key, value in new_dict.iteritems():
            if str(key) == 'type':
                data['data']['type'] = str(value)
            elif str(key) == 'id':
                data['data']['id'] = str(value)
            elif isinstance(value, list):
                lst = []
                for index in range(len(value)):
                    if isinstance(value[index], dict):
                        lst.append(dict_iterate(value[index]))
                    else:
                        lst.append(value[index])
                attributes[key] = lst
            else:
                attributes[key] = value
        data['data']['attributes'] = attributes
    return data


def create_error_422(source, message):
    errors = {'errors': [{'status':'422'}]}
    errors['errors'][0]['source'] = str(source)
    errors['errors'][0]['details'] = message
    json_errors = Response(json.dumps(errors, indent=2), content_type="application/vnd.api+json", status=422)
    print json_errors
    return json_errors


def parse_and_return(response):
    output = json_api_parser(response)
    json_output = Response(json.dumps(output, indent=2), content_type='application/json')
    print json_output
    return json_output


