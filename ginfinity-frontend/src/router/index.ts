import { createWebHistory, createRouter } from 'vue-router'; // Cambié createWebHashHistory por createWebHistory
import HomeView from '../views/HomeView.vue';
import ComparadorARN from '../views/ComparadorARN.vue'; // Importa la vista ComparadorARN
import EmbeddingARN from '../views/EmbeddingARN.vue'; // Correcto import
import CalcularEmbeddings from '../views/CalcularEmbeddings.vue'; // Importa la nueva vista

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'Home' }, // Establecer un título para esta ruta
  },
  {
    path: '/comparar-arn',
    name: 'comparador-arn',
    component: ComparadorARN,
    meta: { title: 'Comparar ARN' },  // Título personalizado para esta ruta
  },
  {
    path: '/embedding-arn',
    name: 'embedding-arn',
    component: EmbeddingARN,
    meta: { title: 'Embedding ARN' },  // Título personalizado para esta ruta
  },
  {
    path: '/calcular-embeddings', // Ruta para la nueva vista
    name: 'calcular-embeddings',
    component: CalcularEmbeddings,
    meta: { title: 'Calcular Embeddings' }, // Título para esta ruta
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),  // Usé createWebHistory en lugar de createWebHashHistory
  routes,
});

export default router;
