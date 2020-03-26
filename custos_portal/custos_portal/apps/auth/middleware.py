

def gateway_groups_middleware(get_response):
    """Add 'is_gateway_admin' and 'is_read_only_gateway_admin' to request."""
    def middleware(request):
        request.is_gateway_admin = False
        if request.user.is_authenticated and request.session.get('GATEWAY_GROUPS'):
            gateway_groups = request.session['GATEWAY_GROUPS']
            request.is_gateway_admin = 'admin' in gateway_groups
        return get_response(request)
    return middleware
