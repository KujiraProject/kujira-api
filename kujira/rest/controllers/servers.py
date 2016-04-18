import json

from kujira.blueprints import server_bp
from kujira.rest.lib.helper_methods import arg_parser_init, authenticate, print_and_return


@server_bp.route("")
def server():
    args, remainder = arg_parser_init('server').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))

@server_bp.route("/<fsid>")
def server_fsid(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid).parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))

@server_bp.route("/<fsid>/<fqdn>")
def server_fsid_fqdn(fsid, fqdn):
    args, remainder = arg_parser_init('cluster/'+fsid+'/server/'+fqdn).parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


