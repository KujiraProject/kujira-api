import json

from kujira.blueprints import cluster_bp
from kujira.rest.lib.helper_methods import arg_parser_init, print_and_return, generate_response



@cluster_bp.route("")
def cluster():
    args, remainder = arg_parser_init('cluster').parse_known_args()
    response = generate_response(args)
    return print_and_return(response)
