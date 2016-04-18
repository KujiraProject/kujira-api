import json

from kujira.blueprints import mon_bp
from kujira.rest.lib.helper_methods import arg_parser_init, authenticate, print_and_return


@mon_bp.route("/<fsid>")
def mon_fsid(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/mon').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))