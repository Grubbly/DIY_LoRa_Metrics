import Vue from "vue";
import App from "./App";
import * as VueGoogleMaps from "vue2-google-maps";

var creds = require('./creds.json')

Vue.config.productionTip = false

Vue.use(VueGoogleMaps, {
  load: {
    key: creds.api_key,
    libraries: "places" // necessary for places input
  }
});

new Vue({
  render: h => h(App),
}).$mount('#app')
