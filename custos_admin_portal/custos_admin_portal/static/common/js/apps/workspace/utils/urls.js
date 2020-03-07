export default {

  viewTenantRequest(tenantRequest) {
    return (
      "/workspace/request/" +
      encodeURIComponent(tenantRequest.requestId) +
      "/"
    );
  },
  navigateToViewRequest(tenantRequest) {
    window.location.assign(
      this.viewTenantRequest(tenantRequest)
    );
  }
};
