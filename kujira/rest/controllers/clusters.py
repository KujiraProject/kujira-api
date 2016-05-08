from kujira.blueprints import cluster_bp
from kujira.rest.lib.request_methods import send_get_alt
from kujira.rest.lib.parsing_methods import parse_and_return


@cluster_bp.route("")
def cluster():
    response = send_get_alt('cluster')
    return parse_and_return(clusters_parse, response)


def clusters_parse(json_dict):
    try:
        new_dict = json_dict[0]
    except Exception as e:
        new_dict = json_dict
        print e.message
    data = {'data': {'type' : 'cluster'}}
    attributes = {}
    if new_dict:
        for key, value in new_dict.iteritems():
            if str(key) == 'name':
                data['data']['id'] = str(value)
                attributes[key] = value
            else:
                attributes[key] = value
        data['data']['attributes'] = attributes
    return data