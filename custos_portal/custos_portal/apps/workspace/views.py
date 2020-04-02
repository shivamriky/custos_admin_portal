import logging
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def request_new_tenant(request):
    if request.method == 'POST':
        logger.debug("Form is posted")
    request.active_nav_item = 'request-new-tenant'

    return render(request, 'workspace/request_new_tenant.html', {
        'bundle_name': 'request-new-tenant',
    })


def list_new_tenant_requests(request):
    request.active_nav_item = 'list-requests'
    if request.user:
        print("hell")
    return render(request, 'workspace/list_requests.html', {
        'bundle_name': 'list-requests',
    })


def view_tenant_request(request, tenant_request_id):
    return render(request, 'workspace/view_tenant_request.html', {
        'bundle_name': 'view-request',
        'tenant_request_id': tenant_request_id
    })
