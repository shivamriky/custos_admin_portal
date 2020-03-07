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
      this.viewTenantRequest(tenantRequest)
    );
  }
};
