import { createApp } from 'vue';
import App from './App.vue';
import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import router from './router';
import './assets/styles.css';

const vuetify = createVuetify();

createApp(App)
  .use(vuetify)
  .use(router) 
  .mount('#app');
