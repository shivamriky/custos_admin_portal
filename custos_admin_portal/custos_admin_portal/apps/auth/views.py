from django.conf import settings
from django.forms import formset_factory
from django.shortcuts import render

from . import forms


def start_login(request):
    return render(request, 'custos_admin_portal_auth/login.html', {
        'next': request.GET.get('next', None),
        'options': settings.AUTHENTICATION_OPTIONS,
    })


def redirect_login(request, idp_alias):
    print("redirect login is called")


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
                success = iam_admin_client.register_user(
                    username, email, first_name, last_name, password)
                if not success:
                    form.add_error(None, ValidationError(
                        "Failed to register user with IAM service"))
                else:
                    _create_and_send_email_verification_link(
                        request, username, email, first_name, last_name)
                    messages.success(
                        request,
                        "Account request processed successfully. Before you "
                        "can login you need to confirm your email address. "
                        "We've sent you an email with a link that you should "
                        "click on to complete the account creation process.")
                    return redirect(
                        reverse('django_airavata_auth:create_account'))
            except Exception as e:
                logger.exception(
                    "Failed to create account for user", exc_info=e)
                form.add_error(None, ValidationError(e.message))
    else:
        form = forms.CreateAccountForm()
    return render(request, 'custos_admin_portal_auth/create_account.html', {
        'options': settings.AUTHENTICATION_OPTIONS,
        'form': form
    })

