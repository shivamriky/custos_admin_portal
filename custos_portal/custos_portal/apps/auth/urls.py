from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'custos_portal_auth'
urlpatterns = [
    path('login/', views.start_login, name='login'),
    url(r'^redirect_login/(\w+)/$', views.redirect_login, name='redirect_login'),
    url(r'^create-account$', views.create_account, name='create_account')
]
