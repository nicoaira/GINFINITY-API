import { createWebHistory, createRouter } from 'vue-router';
import HomeView from '../views/home.vue';
import ComparadorARN from '../views/compare.vue';
import CalcularEmbeddings from '../views/tsv_embed.vue'; 
import Help from '../views/help.vue';
import Results from '../views/results.vue'; 
import JobStatus from '@/components/JobStatus.vue'


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
  },
  {
    path: '/job/:jobId',
    name: 'JobStatus',
    component: JobStatus,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0, behavior: 'smooth' };
    }
  }
});

export default router;
