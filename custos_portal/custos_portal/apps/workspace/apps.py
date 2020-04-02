from custos_portal.app_config import CustosAppConfig


class WorkspaceConfig(CustosAppConfig):
    name = 'custos_portal.apps.workspace'
    label = 'custos_portal_workspace'
    verbose_name = 'Workspace'
    app_order = 0
    url_home = 'custos_portal_workspace:request_new_tenant'
    fa_icon_class = 'fa-flask'
    app_description = """
        Launch applications and manage your experiments and projects.
    """
    nav = [
        {
            'label': 'Create new tenant request',
            'icon': 'fa fa-plus-square',
            'url': 'custos_portal_workspace:request_new_tenant',
            'active_prefixes': ['applications', 'request-new-tenant'],
        },
        {
            'label': 'List of all existing tenant requests',
            'icon': 'fa fa-list',
            'url': 'custos_portal_workspace:list_requests',
            'active_prefixes': ['applications', 'list-requests'],
        }
    ]

    def app_enabled(self, request):
        return True
