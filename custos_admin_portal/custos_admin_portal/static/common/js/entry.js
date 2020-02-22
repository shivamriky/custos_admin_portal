import Vue from "vue";
import BootstrapVue from "bootstrap-vue";

// This is imported globally on the website (see main.js) so no need to include
// it again in this view
// import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap-vue/dist/bootstrap-vue.css";
import Vuelidate from 'vuelidate'

/**
 * Common entry point function. Sets up common entry point functionality and
 * then calls the passed function with the Vue class as the first argument.
 *
 * @param {Function} entryPointFunction
 */
export default function entry(entryPointFunction) {
  // Common Vue configuration
  Vue.use(BootstrapVue);
  Vue.use(Vuelidate)
  entryPointFunction(Vue);
}
