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
KEYCLOAK_LOGOUT_URL = 'https://keycloak.custos.scigap.org:31000/auth/realms/10000101/protocol/openid-connect/logout'
# Optional: specify if using self-signed certificate or certificate from unrecognized CA
#KEYCLOAK_CA_CERTFILE = os.path.join(BASE_DIR, "django_airavata", "resources", "incommon_rsa_server_ca.pem")
KEYCLOAK_VERIFY_SSL = False


SESSION_COOKIE_SECURE = False

# Default email backend (for local development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Django - Email settings
# Uncomment and specify the following for sending emails (default email backend
# just prints to the console)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = '...'
# EMAIL_PORT = '...'
# EMAIL_HOST_USER = '...'
# EMAIL_HOST_PASSWORD = '...'
# EMAIL_USE_TLS = True
ADMINS = [('Admin Name', 'admin@example.com')]
# SERVER_EMAIL = 'portal@example.com'


# Portal settings
PORTAL_TITLE = 'Custos Admin Portal'
