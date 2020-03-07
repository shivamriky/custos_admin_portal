from django.shortcuts import render


def list_new_tenant_requests(request):
    print("New tenant requests list is called")
    # TODO fetch all the tenant requests from airavata here.
    return render(request, 'workspace/list_requests.html', {
        'bundle_name': 'list-requests',
    })


def view_tenant_request(request, tenant_request_id):
    print("Admin Tenant request Id: {}".format(tenant_request_id)),
    return render(request, 'workspace/view_tenant_request.html', {
        'bundle_name': 'view-request',
        'tenant_request_id': tenant_request_id
    })
