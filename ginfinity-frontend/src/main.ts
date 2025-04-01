import { createApp } from 'vue';
import App from './App.vue';
import { createVuetify } from 'vuetify';
import 'vuetify/styles';
import router from './router'; // Importas el router que ya tienes configurado
import './assets/styles.css';

const vuetify = createVuetify(); // Instancia Vuetify

createApp(App)
  .use(vuetify) // Usas Vuetify
  .use(router)  // Usas Vue Router
  .mount('#app');
