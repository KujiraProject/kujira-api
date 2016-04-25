import json

from kujira.blueprints import mon_bp
from kujira.rest.lib.helper_methods import arg_parser_init, print_and_return, generate_response


@mon_bp.route("/<fsid>")
def all_monitors(fsid):
    args, remainder = arg_parser_init('cluster/' + fsid + '/mon').parse_known_args()
    response = generate_response(args)
    return print_and_return(response)


@mon_bp.route("/<fsid>/<name>")
def monitor(fsid, name):
    args, remainder = arg_parser_init('cluster/' + fsid + '/mon/' + name).parse_known_args()
    response = generate_response(args)
    return print_and_return(response)


@mon_bp.route("/<fsid>/<name>/status")
def monitor_status(fsid, name):
    args, remainder = arg_parser_init('cluster/' + fsid + '/mon/' + name + '/status').parse_known_args()
    response = generate_response(args)
    return print_and_return(response)

