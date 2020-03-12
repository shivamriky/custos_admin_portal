import { entry } from "../../index";
import MainLayout from "../../components/MainLayout";
import EditTenantRequest from "./EditTenantRequest";

// Expect a template with id "edit-experiment" and experiment-id data attribute
//
//   <div id="edit-experiment" data-experiment-id="..expid.."/>

entry(Vue => {
  new Vue({
    render(h) {
      return h(MainLayout, [
        h(EditTenantRequest, {
          props: {
            tenantRequestId: this.tenantRequestId
          }
        })
      ]);
    },
    data() {
      return {
        tenantRequestId: null
      };
    },
    beforeMount() {
      this.tenantRequestId = JSON.parse(this.$el.dataset.tenantRequestId);
      console.log("Entry for admin edit tenant request is executed")
    }
  }).$mount("#admin-edit-request");
});
