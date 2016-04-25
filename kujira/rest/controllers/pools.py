import json

from kujira.blueprints import pool_bp
from kujira.rest.lib.helper_methods import arg_parser_init, print_and_return, generate_response


@pool_bp.route("/<fsid>")
def all_pools(fsid):
    args, remainder = arg_parser_init('cluster/' + fsid + '/pool').parse_known_args()
    response = generate_response(args)
    return print_and_return(response)


@pool_bp.route("/<fsid>/<id>")
def pool(fsid, id):
    args, remainder = arg_parser_init('cluster/' + fsid + '/pool/' + str(id)).parse_known_args()
    response = generate_response(args)
    return print_and_return(response)

