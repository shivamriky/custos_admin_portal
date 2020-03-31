import logging
import json
from time import timezone
from urllib.parse import quote
from datetime import datetime, timedelta, timezone


from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.forms import formset_factory, models
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, resolve_url
from django.template import Context
from django.urls import reverse
from django.utils.http import urlencode
from django.views.decorators.debug import sensitive_variables
from google.protobuf.json_format import MessageToDict
from requests_oauthlib import OAuth2Session

from . import utils
from . import models
from . import forms
from ... import identity_management_client
from ... import user_management_client

logger = logging.getLogger(__name__)


def callback(request):
    try:
        user = authenticate(request=request)
        logger.debug("Saving user to session: {}".format(user))
        login(request, user)
        return _handle_login_redirect(request)
    except Exception as err:
        logger.exception("An error occurred while processing OAuth2 "
                         "callback: {}".format(request.build_absolute_uri()))
        idp_alias = "cilogon"
        return redirect(reverse('custos_portal_auth:callback-error',
                                args=(idp_alias,)))


def callback_error(request, idp_alias):
    _validate_idp_alias(idp_alias)
    # Create a filtered options object with just the given idp_alias
    options = {
        'external': []
    }
    for ext in settings.AUTHENTICATION_OPTIONS['external']:
        if ext['idp_alias'] == idp_alias:
            options['external'].append(ext.copy())

    return render(request, 'custos_portal_auth/callback-error.html', {
        'idp_alias': idp_alias,
        'options': options,
    })


def create_account(request):
    if request.method == 'POST':
        form = forms.CreateAccountForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                password = form.cleaned_data['password']
                is_temp_password = False
                result = user_management_client.register_user(settings.CUSTOS_TOKEN, username, first_name, last_name,
                                                              password, email, is_temp_password)
                if result.is_registered:
                    logger.debug("User account successfully created for : {}".format(username))
                    _create_and_send_email_verification_link(request, username, email, first_name, last_name,
                                                             settings.LOGIN_URL)
                    messages.success(
                        request,
                        "Account request processed successfully. Before you "
                        "can login you need to confirm your email address. "
                        "We've sent you an email with a link that you should "
                        "click on to complete the account creation process.")
                else:
                    form.add_error(None, ValidationError("Failed to register the user with IAM service"))
            except TypeError as e:
                logger.exception(
                    "Failed to create account for user", exc_info=e)
                form.add_error(None, ValidationError(e))
            return render(request, 'custos_portal_auth/create_account.html', {
                'options': settings.AUTHENTICATION_OPTIONS,
                'form': form
            })
    else:
        form = forms.CreateAccountForm()
    return render(request, 'custos_portal_auth/create_account.html', {
        'options': settings.AUTHENTICATION_OPTIONS,
        'form': form
    })


def forgot_password(request):
    if request.method == 'POST':
        form = forms.ForgotPasswordForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                if not user_management_client.is_username_available(settings.CUSTOS_TOKEN, username).is_exist:
                    if not user_management_client.is_user_enabled(settings.CUSTOS_TOKEN, username).is_exist:
                        messages.error(
                            request,
                            "Please finish creating your account before "
                            "resetting your password. Provide your username "
                            "below and we will send you another email "
                            "verification link.")
                        return redirect(
                            reverse('custos_portal_auth:resend_email_link'))
                    _create_and_send_password_reset_request_link(request, username)
                # Always display this message even if you doesn't exist. Don't
                # reveal whether a user with that username exists.
                messages.success(
                    request,
                    "Reset password request processed successfully. We've "
                    "sent an email with a password reset link to the email "
                    "address associated with the username you provided. You "
                    "can use that link within the next 24 hours to set a new "
                    "password.")
                return redirect(
                    reverse('custos_portal_auth:forgot_password'))
            except Exception as e:
                logger.exception(
                    "Failed to generate password reset request for user",
                    exc_info=e)
                form.add_error(None, ValidationError(str(e)))
    else:
        form = forms.ForgotPasswordForm()
    return render(request, 'custos_portal_auth/forgot_password.html', {
        'form': form
    })


def _create_and_send_password_reset_request_link(request, username):
    password_reset_request = models.PasswordResetRequest(username=username)
    password_reset_request.save()

    verification_uri = request.build_absolute_uri(
        reverse(
            'custos_portal_auth:reset_password', kwargs={
                'code': password_reset_request.reset_code}))
    logger.debug(
        "password reset verification_uri={}".format(verification_uri))

    user = user_management_client.get_user(settings.CUSTOS_TOKEN, username)
    context = Context({
        "username": username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "portal_title": settings.PORTAL_TITLE,
        "url": verification_uri,
    })
    utils.send_email_to_user(models.PASSWORD_RESET_EMAIL_TEMPLATE, context)


def handle_login(request):
    username = request.POST['username']
    password = request.POST['password']
    login_type = request.POST.get('login_type', None)
    template = "custos_portal_auth/login.html"
    if login_type and login_type == 'password':
        template = "custos_portal_auth/login_username_password.html"
    user = authenticate(username=username, password=password, request=request)
    logger.debug("authenticated user: {}".format(user))
    try:
        if user is not None:
            login(request, user)
            return _handle_login_redirect(request)
        else:
            messages.error(request, "Login failed. Please try again.")
    except Exception as err:
        messages.error(request,
                       "Login failed: {}. Please try again.".format(str(err)))
    return render(request, template, {
        'username': username,
        'next': request.POST.get('next', None),
        'options': settings.AUTHENTICATION_OPTIONS,
        'login_type': login_type,
    })


def redirect_login(request, idp_alias):
    _validate_idp_alias(idp_alias)

    client_id = settings.KEYCLOAK_CLIENT_ID

    auth_base_url = identity_management_client.get_oidc_configuration(settings.CUSTOS_TOKEN, client_id)
    # auth_base_url = json.loads(auth_base_url.)
    # print(auth_base_url)
    base_authorize_url = settings.KEYCLOAK_AUTHORIZE_URL

    redirect_uri = request.build_absolute_uri(
        reverse('custos_portal_auth:callback'))

    oauth2_session = OAuth2Session(
        client_id, scope='openid', redirect_uri=redirect_uri)
    authorization_url, state = oauth2_session.authorization_url(
        base_authorize_url)
    authorization_url += '&kc_idp_hint=' + quote("oidc")

    # Store state in session for later validation (see backends.py)
    request.session['OAUTH2_STATE'] = state
    request.session['OAUTH2_REDIRECT_URI'] = redirect_uri

    logger.debug('Redirect URI: {}'.format(redirect_uri))
    logger.debug('Authorization URL for OpenID: {}'.format(authorization_url))
    return redirect(authorization_url)


def resend_email_link(request):
    if request.method == 'POST':
        form = forms.ResendEmailVerificationLinkForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                if not user_management_client.is_username_available(settings.CUSTOS_TOKEN, username).is_exist:
                    user_profile = user_management_client.get_user(settings.CUSTOS_TOKEN, username)
                    print(user_profile)
                    _create_and_send_email_verification_link(
                        request,
                        username,
                        user_profile.email,
                        user_profile.first_name,
                        user_profile.last_name,
                        settings.LOGIN_URL)
                    messages.success(
                        request,
                        "Email verification link sent successfully. Please "
                        "click on the link in the email that we sent "
                        "to your email address.")
                else:
                    messages.error(
                        request,
                        "Unable to resend email verification link. Please "
                        "contact the website administrator for further "
                        "assistance.")
                return redirect(
                    reverse('custos_portal_auth:resend_email_link'))
            except Exception as e:
                logger.exception(
                    "Failed to resend email verification link", exc_info=e)
                form.add_error(None, ValidationError(str(e)))
    else:
        form = forms.ResendEmailVerificationLinkForm()
    return render(request, 'custos_portal_auth/verify_email.html', {
        'form': form
    })


@sensitive_variables('password')
def reset_password(request, code):
    try:
        password_reset_request = models.PasswordResetRequest.objects.get(
            reset_code=code)
    except ObjectDoesNotExist as e:
        messages.error(
            request,
            "Reset password link is invalid. Please try again.")
        return redirect(reverse('custos_portal_auth:forgot_password'))

    now = datetime.now(timezone.utc)
    if now - password_reset_request.created_date > timedelta(days=1):
        password_reset_request.delete()
        messages.error(
            request,
            "Reset password link has expired. Please try again.")
        return redirect(reverse('custos_portal_auth:forgot_password'))

    if request.method == "POST":
        form = forms.ResetPasswordForm(request.POST)
        if form.is_valid():
            try:
                password = form.cleaned_data['password']
                # TODO Password is not updating properly
                success = user_management_client.reset_password(settings.CUSTOS_TOKEN, password_reset_request.username,
                                                                password)
                logger.debug("Password reset result: {}".format(success))
                if not success:
                    messages.error(
                        request, "Failed to reset password. Please try again.")
                    return redirect(
                        reverse('custos_portal_auth:forgot_password'))
                else:
                    password_reset_request.delete()
                    messages.success(
                        request,
                        "You may now log in with your new password.")
                    return redirect(
                        reverse('custos_portal_auth:login_with_password'))
            except Exception as e:
                logger.exception(
                    "Failed to reset password for user", exc_info=e)
                form.add_error(None, ValidationError(str(e)))
    else:
        form = forms.ResetPasswordForm()
    return render(request, 'custos_portal_auth/reset_password.html', {
        'form': form,
        'code': code
    })


def start_login(request):
    return render(request, 'custos_portal_auth/login.html', {
        'next': request.GET.get('next', None),
        'options': settings.AUTHENTICATION_OPTIONS,
    })


def start_logout(request):
    logout(request)
    redirect_url = request.build_absolute_uri(resolve_url(settings.LOGOUT_REDIRECT_URL))
    return redirect(settings.KEYCLOAK_LOGOUT_URL + "?redirect_uri=" + quote(redirect_url))


def start_username_password_login(request):
    # return bad request if password isn't a configured option
    if 'password' not in settings.AUTHENTICATION_OPTIONS:
        return HttpResponseBadRequest("Username/password login is not enabled")
    return render(request,
                  'custos_portal_auth/login_username_password.html',
                  {
                      'next': request.GET.get('next', None),
                      'options': settings.AUTHENTICATION_OPTIONS,
                      'login_type': 'password'
                  })


def verify_email(request, code):
    try:
        email_verification = models.EmailVerification.objects.get(verification_code=code)
        email_verification.verified = True
        email_verification.save()
        # Check if user is enabled, if so redirect to login page
        username = email_verification.username
        logger.debug("Email address verified for {}".format(username))
        login_url = reverse('custos_portal_auth:login')
        if email_verification.next:
            login_url += "?" + urlencode({'next': email_verification.next})

        print(user_management_client.is_user_enabled(settings.CUSTOS_TOKEN, "shivam_testing_3"))
        if user_management_client.is_user_enabled(settings.CUSTOS_TOKEN, username).is_exist:
            logger.debug("User {} is already enabled".format(username))
            messages.success(
                request,
                "Your account has already been successfully created. "
                "Please log in now.")
            return redirect(login_url)
        else:
            logger.debug("Enabling user {}".format(username))
            # enable user and inform admins
            user_profile = MessageToDict(user_management_client.enable_user(settings.CUSTOS_TOKEN, username))
            logger.debug(user_profile)
            email_address = user_profile["email"]
            first_name = user_profile["firstName"]
            last_name = user_profile["lastName"]
            utils.send_new_user_email(request,
                                      username,
                                      email_address,
                                      first_name,
                                      last_name)
            messages.success(
                request,
                "Your account has been successfully created. "
                "Please log in now.")
            return redirect(login_url)
    except ObjectDoesNotExist as e:
        # if doesn't exist, give user a form where they can enter their
        # username to resend verification code
        logger.exception("EmailVerification object doesn't exist for "
                         "code {}".format(code))
        messages.error(
            request,
            "Email verification failed. Please enter your username and we "
            "will send you another email verification link.")
        return redirect(reverse('custos_portal_auth:resend_email_link'))
    except Exception as e:
        logger.exception("Email verification processing failed!")
        messages.error(
            request,
            "Email verification failed. Please try clicking the email "
            "verification link again later.")
        return redirect(reverse('custos_portal_auth:create_account'))


def _create_and_send_email_verification_link(request, username, email, first_name, last_name, next_url=None):
    email_verification = models.EmailVerification(username=username, next=next_url)
    email_verification.save()

    verification_uri = request.build_absolute_uri(
        reverse('custos_portal_auth:verify_email', kwargs={'code': email_verification.verification_code}))
    logger.debug(
        "verification_uri={}".format(verification_uri))

    context = Context({
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "portal_title": settings.PORTAL_TITLE,
        "url": verification_uri,
    })
    utils.send_email_to_user(models.VERIFY_EMAIL_TEMPLATE, context)


def _validate_idp_alias(idp_alias):
    external_auth_options = settings.AUTHENTICATION_OPTIONS['external']
    valid_idp_aliases = [ext['idp_alias'] for ext in external_auth_options]
    if idp_alias not in valid_idp_aliases:
        raise Exception("idp_alias is not valid: {}".format(idp_alias))


def _handle_login_redirect(request):
    if request.is_gateway_admin:
        return redirect(reverse('custos_portal_admin:list_requests'))
    else:
        return redirect(reverse('custos_portal_workspace:list_requests'))
