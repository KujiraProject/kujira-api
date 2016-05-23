"""
Configuration file.
"""

DEBUG = True

# Server config
HOST = 'localhost'
#HOST = '0.0.0.0'
PORT = 5000

# Secret key for signing cookies
SECRET_KEY = "secret"

# Default Calamari API url
CALAMARI_API_URL = "http://localhost/api/v2/"

# Default Calamari API username
CALAMARI_API_USER = "admin"

# Default Calamari API password
CALAMARI_API_PWD = "kujira"

# Default timetout when connecting calamari api
CALAMARI_API_TIMEOUT = 2
