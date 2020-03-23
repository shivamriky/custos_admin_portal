import { entry } from "../../index";
import ListTenantRequestsContainer from "./ListTenantRequestsContainer";
import MainLayout from "../../components/MainLayout";

// Expect a template with id "edit-experiment" and experiment-id data attribute
//
//   <div id="edit-experiment" data-experiment-id="..expid.."/>

entry(Vue => {
  new Vue({
    render(h) {
      return h(MainLayout, [
        h(ListTenantRequestsContainer)
      ]);
    },
    data() {
      return {
        experimentId: null
      };
    },
    beforeMount() {
      console.log("Entry for list-new-tenant-request is executed")
    }
  }).$mount("#list-requests");
});
