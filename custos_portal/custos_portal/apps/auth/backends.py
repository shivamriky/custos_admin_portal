import logging

from django.contrib.auth.models import User
from django.views.decorators.debug import sensitive_variables

logger = logging.getLogger(__name__)


class CustosAuthBackend(object):
    """Django authentication backend for custos admin portal"""

    @sensitive_variables('password')
    def authenticate(self, request=None, username=None, password=None, refresh_token=None):
        if username and password:
            return

        return None

    def get_user(self, user_id):
        try:
            User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def _process_userinfo(self, request, userinfo):
        logger.debug("userinfo: {}".format(userinfo))
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
            # Save the user locally in Django database
            user.save()
        except User.DoesNotExist:
            user = User(username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email)
            user.save()
        return user
