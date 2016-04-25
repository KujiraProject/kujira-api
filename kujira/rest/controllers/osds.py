import json

from kujira.blueprints import osd_bp
from kujira.rest.lib.helper_methods import arg_parser_init, print_and_return, generate_response


@osd_bp.route("/<fsid>")
def all_osds(fsid):
    args, remainder = arg_parser_init('cluster/' + fsid + '/osd').parse_known_args()
    response = generate_response(args)
    return print_and_return(response)


@osd_bp.route("/<fsid>/<id>")
def osd(fsid, id):
    args, remainder = arg_parser_init('cluster/' + fsid + '/osd/' + id).parse_known_args()
    response = generate_response(args)
    return print_and_return(response)
