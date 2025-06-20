<template>
  <div>
    <h2>Estado del Job {{ jobId }}</h2>
    <div v-if="loading">Procesando... Por favor espera.</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="result">
      <p>Similitud: {{ result.similarity_score }}</p>
      <!-- Aquí muestra más datos que retorne el job -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const jobId = route.params.jobId
const loading = ref(true)
const error = ref(null)
const result = ref(null)

async function checkJobStatus() {
  try {
    const res = await fetch(`/job-status/${jobId}`)
    if (!res.ok) throw new Error(`Error HTTP: ${res.status}`)
    const data = await res.json()
    if (data.finished) {
      result.value = data.result // o como se llame el resultado final
      loading.value = false
    } else {
      setTimeout(checkJobStatus, 2000) // espera 2s y pregunta otra vez
    }
  } catch (err) {
    error.value = err.message
    loading.value = false
  }
}

onMounted(() => {
  checkJobStatus()
})
</script>
