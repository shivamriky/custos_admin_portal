from django.conf.urls import url

from . import views

app_name = 'custos_admin_portal_workspace'
urlpatterns = [
    url(r'^request-new-tenant', views.request_new_tenant, name='request_new_tenant'),
    url(r'^list-requests', views.list_new_tenant_requests, name='list_requests'),
    url(r'request/(?P<tenant_request_id>[^/]+)/$', views.view_tenant_request, name="view_tenant_request")
]
