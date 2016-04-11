import argparse
import json

from flask import Flask

from AuthenticatedHttpClient import AuthenticatedHttpClient

app = Flask(__name__)

# Calamari API url
url = 'http://localhost/api/v2/'


# Helpers
def print_and_return(response):
    print response
    return response


def arg_parser_init(url_str):
    p = argparse.ArgumentParser()
    p.add_argument('--user', default='admin')
    p.add_argument('--pass', dest='password', default='kujira')
    p.add_argument('-u', dest='url', default=url_str)
    return p


def auth(arg_user, arg_pwd):
    c = AuthenticatedHttpClient(url, arg_user, arg_pwd)
    c.login()
    return c


# Endpoints
@app.route("/")
def hello():
    return "Flask calamari wrapper!"


@app.route("/server")
def login():
    args, remainder = arg_parser_init('server').parse_known_args()
    response = auth(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


@app.route("/osd/<fsid>")
def osd(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/osd').parse_known_args()
    response = auth(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


@app.route("/osd_config/<fsid>")
def osd_config(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/osd_config').parse_known_args()
    response = auth(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


@app.route("/osd_id/<fsid>/<int:id>")
def osd_id(fsid, id):
    args, remainder = arg_parser_init('cluster/'+fsid+'/osd/'+str(id)).parse_known_args()
    response = auth(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


@app.route("/pool/<fsid>")
def pool(fsid):
    args, remainder = arg_parser_init('cluster/'+fsid+'/pool').parse_known_args()
    response = auth(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


@app.route("/pool_id/<fsid>/<int:id>")
def pool_id(fsid, id):
    args, remainder = arg_parser_init('cluster/'+fsid+'/pool/'+str(id)).parse_known_args()
    response = auth(args.user, args.password).request('GET', args.url).json()
    return print_and_return(json.dumps(response, indent=2))


if __name__ == "__main__":
    app.run(host='0.0.0.0')



