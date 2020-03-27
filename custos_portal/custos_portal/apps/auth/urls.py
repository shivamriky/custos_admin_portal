from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'custos_portal_auth'
urlpatterns = [
    path('login/', views.start_login, name='login'),
    url(r'^redirect_login/(\w+)/$', views.redirect_login, name='redirect_login'),
    url(r'^create-account$', views.create_account, name='create_account'),
    url(r'^redirect_login/(\w+)/$', views.redirect_login, name='redirect_login'),
    url(r'^callback/$', views.callback, name='callback'),
    url(r'^callback-error/(?P<idp_alias>\w+)/$', views.callback_error,
        name='callback-error'),
    url(r'handle-login', views.handle_login, name="handle_login"),
    url(r'^logout$', views.start_logout, name='logout'),
    url(r'^verify-email/(?P<code>[\w-]+)/$', views.verify_email,
        name="verify_email"),

]
