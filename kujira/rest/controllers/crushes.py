import json

from kujira.blueprints import crush_bp
from kujira.rest.lib.helper_methods import arg_parser_init, authenticate, print_and_return

@crush_bp.route("/<fsid>/crush_map")
def crush_map(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/crush_map').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))

@crush_bp.route("/<fsid>/crush_node")
def crush_node(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/crush_node').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))

@crush_bp.route("/<fsid>/crush_rule")
def crush_rule(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/crush_rule').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))

@crush_bp.route("/<fsid>/crush_rule_set")
def crush_rule_set(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/crush_rule_set').parse_known_args()
    response = authenticate(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))