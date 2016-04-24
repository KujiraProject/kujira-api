import json

from kujira.blueprints import cluster_bp
from kujira.rest.lib.helper_methods import arg_parser_init, authenticate, print_and_return


@cluster_bp.route("")
def cluster():
    args, remainder = arg_parser_init('cluster').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))
