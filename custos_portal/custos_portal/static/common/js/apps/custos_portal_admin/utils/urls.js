export default {

  viewAdminTenantRequest(tenantRequest) {
    return (
      "/admin/request/" +
      encodeURIComponent(tenantRequest.requestId) +
      "/"
    );
  },
  navigateToAdminViewRequest(tenantRequest) {
    window.location.assign(
      this.viewAdminTenantRequest(tenantRequest)
    );
  },
  adminEditTenantRequest(tenantRequest) {
    return (
      "/admin/edit-tenant-request/" +
      encodeURIComponent(tenantRequest.request_id) +
      "/"
    );
  },
  navigateToAdminEditRequest(tenantRequest) {
    window.location.assign(
      this.adminEditTenantRequest(tenantRequest)
    );
  },

};
