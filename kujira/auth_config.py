# -*- coding: utf-8 -*-

"""Authentication controller configuration"""

# roles from most to least privileged
ROLES = [
    'kujira_superusers',
    'kujira_admins',
    'kujira_users'
]

# token lifetime in seconds
TOKEN_LIFETIME = 120

# refresh token lifetime in seconds (-1 == inf)
REFRESH_TOKEN_LIFETIME = 240
