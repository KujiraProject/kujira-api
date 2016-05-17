# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.

# Secret key for signing cookies
SECRET_KEY = "secret"

# Default Calamari API url
CALAMARI_API_URL = "http://192.168.244.1/api/v2/"

# Default Calamari API username
CALAMARI_API_USER = "admin"

# Default Calamari API password
CALAMARI_API_PWD = "kujira"

# Default timetout when connecting calamari api
CALAMARI_API_TIMEOUT = 2