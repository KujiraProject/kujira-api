import json

from kujira.blueprints import mon_bp
from kujira.rest.lib.helper_methods import arg_parser_init, authenticate, print_and_return, create_error_422, \
    parse_and_return


@mon_bp.route("/<fsid>")
def all_monitors(fsid):
    args, remainder = arg_parser_init('cluster/' + fsid + '/mon').parse_known_args()
    try:
        response = authenticate(args.user, args.password).request('GET', args.url).json()
    except Exception as e:
        response = create_error_422(args.url, e.message)
        return print_and_return(response)
    return parse_and_return(response)


@mon_bp.route("/<fsid>/<name>")
def monitor(fsid, name):
    args, remainder = arg_parser_init('cluster/' + fsid + '/mon/' + name).parse_known_args()
    try:
        response = authenticate(args.user, args.password).request('GET', args.url).json()
    except Exception as e:
        response = create_error_422(args.url, e.message)
        return print_and_return(response)
    return parse_and_return(response)


@mon_bp.route("/<fsid>/<name>/status")
def monitor_status(fsid, name):
    args, remainder = arg_parser_init('cluster/' + fsid + '/mon/' + name + '/status').parse_known_args()
    try:
        response = authenticate(args.user, args.password).request('GET', args.url).json()
    except Exception as e:
        response = create_error_422(args.url, e.message)
        return print_and_return(response)
    return parse_and_return(response)

