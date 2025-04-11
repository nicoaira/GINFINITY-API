import { createWebHistory, createRouter } from 'vue-router';
import HomeView from '../views/home.vue';
import ComparadorARN from '../views/compare.vue';
import CalcularEmbeddings from '../views/tsv_embed.vue'; 
import Help from '../views/help.vue';
import Results from '../views/results.vue'; 


const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Home' }, 
  },
  {
    path: '/comparar-arn',
    name: 'comparador-arn',
    component: ComparadorARN,
    meta: { title: 'Comparar ARN' },  
  },
  {
    path: '/calcular-embeddings', 
    name: 'calcular-embeddings',
    component: CalcularEmbeddings,
    meta: { title: 'Calcular Embeddings' }, 
  },
  {
    path: '/help',
    name: 'help',
    component: Help,
    meta: { title: 'Help' },
  },
  {
    path: '/results', 
    name: 'results',
    component: Results,
    meta: { title: 'Results' }, 
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
