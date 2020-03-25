import logging

from clients.user_management_client import UserManagementClient
from custos.core import IamAdminService_pb2
from django import forms
from django.conf import settings
from django.core import validators

logger = logging.getLogger(__name__)
user_management_client = UserManagementClient()

USERNAME_VALIDATOR = validators.RegexValidator(
    regex=r"^[a-z0-9_-]+$",
    message="Username can only contain lowercase letters, numbers, "
            "underscores and hyphens."
)
PASSWORD_VALIDATOR = validators.RegexValidator(
    regex=r"^.*(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[@!$#*&]).*$",
    message="Password needs to contain at least (a) One lower case letter (b) "
            "One Upper case letter and (c) One number (d) One of the following"
            " special characters - !@#$&*"
)


class RegisterNewTenant(forms.Form):
    err_css_class = "is-invalid"
    client_name = forms.CharField(
        label='Client Name',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Client Name'}))
    requester_email = forms.EmailField(
        label='Requester E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'email@example.com'}))
    admin_username = forms.CharField(
        label='Admin Username',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Username'}),
        min_length=6,
        validators=[USERNAME_VALIDATOR],
        help_text=USERNAME_VALIDATOR.message)
    admin_first_name = forms.CharField(
        label='Admin First Name',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'First Name'}))
    admin_last_name = forms.CharField(
        label='Admin Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Last Name'}))
    admin_email = forms.EmailField(
        label='Admin E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'email@example.com'}))
    email_again = forms.EmailField(
        label='E-mail (again)',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com (again)'}))

    domain = forms.CharField(
        label='Domain',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'idp.htrc.indiana.edu'}))
    contacts = forms.CharField(
        label='Domain',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Enter semicolon separated contact numbers'}))
    scope = forms.CharField(
        label='Scope',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'openid profile email org.cilogon.userinfo'}))
    admin_password = forms.CharField(
        label='Admin Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password'}),
        min_length=8,
        max_length=48,
        validators=[PASSWORD_VALIDATOR],
        help_text=PASSWORD_VALIDATOR.message)

    password_again = forms.CharField(
        label='Password (again)',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password (again)'}))
    redirect_uris = forms.CharField(
        label='Domain',
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'rows': 4, 'cols': 60,
                                     'placeholder': '"http://idp.htrc.indiana.edu","http://idp.htrc.indiana.edu"'}),
        help_text="Enter comma separated redirect URLs."
    )
    client_uri = forms.URLField(
        label='Client URL',
        widget=forms.URLInput(attrs={'class': 'form-control',
                                     'placeholder': 'https://idp.htrc.indiana.edu/playground2'}))
    logo_uri = forms.URLField(
        label='Logo URL',
        widget=forms.URLInput(attrs={'class': 'form-control',
                                     'placeholder': 'https://idp.htrc.indiana.edu/playground2'}))
    application_type = forms.CharField(
        label='Application Type',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'web'}))
    comment = forms.CharField(
        label='Comment',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Comment'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')

        if password and password_again and password != password_again:
            self.add_error(
                'password',
                forms.ValidationError("Passwords do not match"))
            self.add_error(
                'password_again',
                forms.ValidationError("Passwords do not match"))

        email = cleaned_data.get('email')
        email_again = cleaned_data.get('email_again')
        if email and email_again and email != email_again:
            self.add_error(
                'email',
                forms.ValidationError("E-mail addresses do not match")
            )
            self.add_error(
                'email_again',
                forms.ValidationError("E-mail addresses do not match")
            )

        username = cleaned_data.get('username')
        # Check here if username is available.
        try:
            if username:
                self.add_error(
                    'username',
                    forms.ValidationError("That username is not available")
                )
        except Exception as e:
            logger.exception("Failed to check if username is available")
            self.add_error(
                'username',
                forms.ValidationError("Error occurred while checking if "
                                      "username is available: " + str(e)))

        return cleaned_data


class CreateAccountForm(forms.Form):
    error_css_class = "is-invalid"
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Username'}),
        min_length=6,
        validators=[USERNAME_VALIDATOR],
        help_text=USERNAME_VALIDATOR.message)
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password'}),
        min_length=8,
        max_length=48,
        validators=[PASSWORD_VALIDATOR],
        help_text=PASSWORD_VALIDATOR.message)
    password_again = forms.CharField(
        label='Password (again)',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password (again)'}))
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': 'email@example.com'}))
    email_again = forms.EmailField(
        label='E-mail (again)',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com (again)'}))
    first_name = forms.CharField(
        label='First Name',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'First Name'}))
    last_name = forms.CharField(
        label='Last Name',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Last Name'}))

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')

        if password and password_again and password != password_again:
            self.add_error(
                'password',
                forms.ValidationError("Passwords do not match"))
            self.add_error(
                'password_again',
                forms.ValidationError("Passwords do not match"))

        email = cleaned_data.get('email')
        email_again = cleaned_data.get('email_again')
        if email and email_again and email != email_again:
            self.add_error(
                'email',
                forms.ValidationError("E-mail addresses do not match")
            )
            self.add_error(
                'email_again',
                forms.ValidationError("E-mail addresses do not match")
            )

        username = cleaned_data.get('username')

        check_username = user_management_client.is_username_available(settings.CUSTOS_TOKEN, username)
        print(check_username.is_exist)
        try:
            if user_management_client.is_username_available(settings.CUSTOS_TOKEN, username).is_exist:
                logger.info("Username is available");
            else:
                logger.info("Username is not available");
                self.add_error(
                    'username',
                    forms.ValidationError("That username is not available")
                )
        except Exception as e:
            self.add_error(
                'username',
                forms.ValidationError("Error occurred while checking the username.")
            )
            logger.info("Username is not available")
        return cleaned_data


class ResendEmailVerificationLinkForm(forms.Form):
    error_css_class = "is-invalid"
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Username'}),
        min_length=6,
        validators=[USERNAME_VALIDATOR])


class ForgotPasswordForm(forms.Form):
    error_css_class = "is-invalid"
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Username'}),
        min_length=6,
        validators=[USERNAME_VALIDATOR],
        help_text=USERNAME_VALIDATOR.message)


class ResetPasswordForm(forms.Form):
    error_css_class = "is-invalid"

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password'}),
        min_length=8,
        max_length=48,
        validators=[PASSWORD_VALIDATOR],
        help_text=PASSWORD_VALIDATOR.message)
    password_again = forms.CharField(
        label='Password (again)',
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': 'Password (again)'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')

        if password and password_again and password != password_again:
            self.add_error(
                'password',
                forms.ValidationError("Passwords do not match"))
            self.add_error(
                'password_again',
                forms.ValidationError("Passwords do not match"))

        return cleaned_data
