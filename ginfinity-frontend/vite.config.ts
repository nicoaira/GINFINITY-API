import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/compare': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/tsv_embed': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      // '/send_email': {
      //   target: 'http://localhost:8000',
      //   changeOrigin: true,
      // }
      
    }
  }
})
