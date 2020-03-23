import { entry } from "../../index";
import RequestNewTenantContainer from "./RequestNewTenantContainer";
import MainLayout from "../../components/MainLayout";

// Expect a template with id "edit-experiment" and experiment-id data attribute
//
//   <div id="edit-experiment" data-experiment-id="..expid.."/>

entry(Vue => {
  new Vue({
    render(h) {
      return h(MainLayout, [
        h(RequestNewTenantContainer)
      ]);
    },
    data() {
      return {
        experimentId: null
      };
    },
    beforeMount() {
      console.log("Entry is executed")
    }
  }).$mount("#request-new-tenant");
});
