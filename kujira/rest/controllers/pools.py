import json

from kujira.blueprints import pool_bp
from kujira.rest.lib.helper_methods import arg_parser_init, authenticate, print_and_return


@pool_bp.route("/<fsid>")
def pool(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/pool').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


@pool_bp.route("/id/<fsid>/<int:id>")
def pool_id(fsid, id):
    args, remainder = arg_parser_init('cluster/'+fsid+'/pool/'+str(id)).parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))

