import json

from kujira.blueprints import osd_bp
from kujira.rest.lib.helper_methods import arg_parser_init, authenticate, print_and_return


@osd_bp.route("/<fsid>")
def osd(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/osd').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


@osd_bp.route("/config/<fsid>")
def osd_config(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/osd_config').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


@osd_bp.route("/id/<fsid>/<int:id>")
def osd_id(fsid, id):
    args, remainder = arg_parser_init('cluster/'+fsid+'/osd/'+str(id)).parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))
