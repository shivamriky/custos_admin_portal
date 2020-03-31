import json
import logging
import time
from pprint import pprint

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.views.decorators.debug import sensitive_variables
from google.auth import jwt
from google.protobuf.json_format import MessageToJson, MessageToDict

from custos_portal import identity_management_client

logger = logging.getLogger(__name__)


class CustosAuthBackend(ModelBackend):
    """Django authentication backend for custos admin portal"""

    @sensitive_variables('password')
    def authenticate(self, request=None, username=None, password=None, refresh_token=None):
        try:
            if username and password:
                token = self._get_token_and_userinfo_password_flow(username, password)
                request.session["ACCESS_TOKEN"] = token
                userinfo = self._get_userinfo_from_token(token)
                self._get_user_groups(request, token)

            # user login using CIlogon
            else:
                token = self._get_token_and_userinfo_redirect_flow(request)
                # the custos api returns different token responses for 'authenticate' and 'token' methods
                userinfo = self._get_userinfo_from_token(token["access_token"])
                self._process_token(request, token)
                self._get_user_groups(request, token["access_token"])

            return self._process_userinfo(request, userinfo)
        except Exception as e:
            logger.exception("login failed")
            return None

    def get_user(self, user_id):
        try:
            logger.debug("Checking for user: {}".format(user_id))
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def _get_token_and_userinfo_password_flow(self, username, password):
        response = identity_management_client.authenticate(settings.CUSTOS_TOKEN, username, password)

        token = MessageToDict(response)["accessToken"]

        logger.debug("Token: {}".format(token))
        return token

    def _get_token_and_userinfo_redirect_flow(self, request):

        code = request.GET.get('code')
        state = request.GET.get('state')
        session_state = request.GET.get('session_state')

        saved_state = request.session['OAUTH2_STATE']
        redirect_uri = request.session['OAUTH2_REDIRECT_URI']
        logger.debug("Code: {}, State: {}, Saved_state: {}, session_state: {}".format(code, state, saved_state,
                                                                                      session_state))

        if state == saved_state:
            response = identity_management_client.token(settings.CUSTOS_TOKEN, redirect_uri, code)
            token = MessageToDict(response)

            logger.debug(token["access_token"])
            return token

        return

    def _process_token(self, request, token):
        # TODO validate the JWS signature
        now = time.time()
        # Put access_token into session to be used for authenticating with API
        # server
        sess = request.session
        sess['ACCESS_TOKEN'] = token['access_token']
        sess['ACCESS_TOKEN_EXPIRES_AT'] = now + token['expires_in']
        sess['REFRESH_TOKEN'] = token['refresh_token']
        sess['REFRESH_TOKEN_EXPIRES_AT'] = now + token['refresh_expires_in']

    def _get_userinfo_from_token(self, token):
        userinfo = {}

        decoded_id_token = jwt.decode(token, verify=False)
        userinfo["username"] = decoded_id_token["preferred_username"]
        userinfo["first_name"] = decoded_id_token["given_name"]
        userinfo["last_name"] = decoded_id_token["family_name"]
        userinfo["email"] = decoded_id_token["email"]
        return userinfo

    def _get_user_groups(self, request, access_token):
        decoded_id_token = jwt.decode(access_token, verify=False)
        user_groups = decoded_id_token["realm_access"]["roles"]
        request.session["GATEWAY_GROUPS"] = user_groups
        request.is_gateway_admin = 'admin' in user_groups

    def _process_userinfo(self, request, userinfo):
        logger.debug("Userinfo: {}".format(userinfo))

        username = userinfo['username']
        email = userinfo['email']
        first_name = userinfo['first_name']
        last_name = userinfo['last_name']

        request.session['USERINFO'] = userinfo

        try:
            user = User.objects.get(username=username)
            # Update these fields each time, in case they have changed
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            logger.debug("User already exists, updating it now")
            # Save the user locally in Django database
            user.save()
        except User.DoesNotExist:
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email)
            logger.debug("User does not already exists, adding it now")
            user.save()
        return user
