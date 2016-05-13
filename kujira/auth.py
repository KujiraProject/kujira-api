# -*- coding: utf-8 -*-

from flask import Response, request, current_app
from flask_pam import Auth
from flask_pam import token
from flask_pam import token_storage
from kujira.blueprints import AUTH_BP
import auth_config
import json

auth = Auth(token_storage.DictStorage,
            token.JWT,
            auth_config.token_lifetime,
            auth_config.refresh_token_lifetime,
            current_app,
            False)

# helper function
def user_role(username):
    role = None
    user_groups = auth.get_groups(username)
    for group in auth_config.roles:
        if group in user_groups:
            role = group
            break

    return role

@AUTH_BP.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    if not ('refresh_token' in data):
        return Response(json.dumps({
            'status': False,
            'errors': [
                'refresh_token is not set'
            ]
        }), mimetype='application/json', status=401)

    refresh_token = data['refresh_token']
    result = auth.refresh(refresh_token)
    
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

        result = auth.authenticate(username, password)
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
