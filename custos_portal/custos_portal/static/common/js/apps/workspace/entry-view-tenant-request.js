import { entry } from "../../index";
import ViewTenantRequestContainer from "./ViewTenantRequestContainer";
import MainLayout from "../../components/MainLayout";

// Expect a template with id "edit-experiment" and experiment-id data attribute
//
//   <div id="edit-experiment" data-experiment-id="..expid.."/>

entry(Vue => {
  new Vue({
    render(h) {
      return h(MainLayout, [
        h(ViewTenantRequestContainer, {
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
      console.log("Entry is executed");
      console.log(this.$el.dataset)
    }
  }).$mount("#view-request");
});
