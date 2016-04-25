import json

from kujira.blueprints import server_bp
from kujira.rest.lib.helper_methods import arg_parser_init, print_and_return, generate_response


@server_bp.route("/<fsid>")
def all_servers(fsid):
    args, remainder = arg_parser_init('cluster/' + fsid + '/server').parse_known_args()
    response = generate_response(args)
    return print_and_return(response)


@server_bp.route("/<fsid>/<fqdn>")
def server(fsid, fqdn):
    args, remainder = arg_parser_init('cluster/' + fsid + '/server/' + fqdn).parse_known_args()
    response = generate_response(args)
    return print_and_return(response)


@server_bp.route("/<fqdn>")
def server_fqdn(fqdn):
    args, remainder = arg_parser_init('server/' + fqdn).parse_known_args()
    response = generate_response(args)
    return print_and_return(response)
