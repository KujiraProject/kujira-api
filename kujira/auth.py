# -*- coding: utf-8 -*-

"""Flask's Blueprint: Authentication"""

import json
from flask import Response, request, current_app
from flask_pam import Auth
from flask_pam import token
from flask_pam import token_storage
from kujira.blueprints import AUTH_BP
from kujira import auth_config

AUTH = Auth(token_storage.DictStorage,
            token.JWT,
            auth_config.TOKEN_LIFETIME,
            auth_config.REFRESH_TOKEN_LIFETIME,
            current_app,
            False)

# helper function
def user_role(username):
    """Return most privileged user's role"""

    role = None
    user_groups = AUTH.get_groups(username)
    for group in auth_config.ROLES:
        if group in user_groups:
            role = group
            break

    return role

@AUTH_BP.route('/refresh', methods=['POST'])
def refresh():
    """Generate new token using refresh token"""

    data = request.get_json()
    if not 'refresh_token' in data:
        return Response(json.dumps({
            'status': False,
            'errors': [
                'refresh_token is not set'
            ]
        }), mimetype='application/json', status=401)

    refresh_token = data['refresh_token']
    result = AUTH.refresh(refresh_token)

    if result[0]:
        return Response(json.dumps({
            'status': True,
            'data': {
                'type': 'tokens',
                'id': result[1].generate(),
                'attributes': {
                    'expire': int(result[1].expire.strftime('%s')),
                },
            }
        }), mimetype='application/json', status=200)

    return Response(json.dumps({
        'status': False,
        'errors': [
            'could not refresh token!',
        ],
    }), mimetype='application/json', status=401)


@AUTH_BP.route('/authenticate', methods=['POST'])
def authenticate():
    """Authenticate user with username and password"""

    if request.method == 'POST':
        data = request.get_json()
        if not ('username' in data and
                'password' in data):
            return Response(json.dumps({
                'status': False,
                'errors': [
                    'username or password is not set!',
                ]
            }), mimetype='application/json', status=401)

        username = data['username'].encode('ascii')
        password = data['password'].encode('ascii')

        result = AUTH.authenticate(username, password)
        role = user_role(username)

        if result[0]:
            return Response(json.dumps({
                'status': True,
                'data': [
                    {
                        'type': 'tokens',
                        'id': result[1].generate(),
                        'attributes': {
                            'expire': int(result[1].expire.strftime('%s')),
                        },
                    },
                    {
                        'type': 'refresh_token',
                        'id': result[2].generate(),
                        'attributes': {
                            'expire': int(result[2].expire.strftime('%s')),
                        },
                    },
                    {
                        'type': 'roles',
                        'id': role,
                    }
                ]
            }), mimetype='application/json', status=200)
        else:
            return Response(json.dumps({
                'status': False,
                'errors': [
                    'authentication failed!',
                ],
            }), mimetype='application/json', status=401)

    return Response(json.dumps({
        'status': False,
        'errors': [
            'bad request type!',
        ]
    }), mimetype='application/json', status=401)
