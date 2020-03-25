"""
Override default Django settings for a particular instance.

Copy this file to settings_local.py and modify as appropriate. This file will
be imported into settings.py last of all so settings in this file override any
defaults specified in settings.py.
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Keycloak Configuration
KEYCLOAK_CLIENT_ID = 'custos-6nwoqodstpe5mvcq09lh-10000101'
KEYCLOAK_CLIENT_SECRET = 'GiKrGGVLW7zDoPZwzgCiFM7WUz3PhIumTmFxAkr7'
KEYCLOAK_AUTHORIZE_URL = 'https://keycloak.custos.scigap.org:31000/auth/realms/10000101/protocol/openid-connect/auth'
KEYCLOAK_TOKEN_URL = 'https://airavata.host:8443/auth/realms/default/protocol/openid-connect/token'
KEYCLOAK_USERINFO_URL = 'https://keycloak.custos.scigap.org:31000/auth/realms/10000101/protocol/openid-connect/auth'
KEYCLOAK_LOGOUT_URL = 'https://airavata.host:8443/auth/realms/default/protocol/openid-connect/logout'
# Optional: specify if using self-signed certificate or certificate from unrecognized CA
#KEYCLOAK_CA_CERTFILE = os.path.join(BASE_DIR, "django_airavata", "resources", "incommon_rsa_server_ca.pem")
KEYCLOAK_VERIFY_SSL = False


SESSION_COOKIE_SECURE = False