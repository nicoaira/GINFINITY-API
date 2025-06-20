<template>
  <div class="comparador">
    <div class="comparador-content">
      <h2 class="compare-title">RNA Sequence Comparator</h2>

      <!-- Explanation Section -->
      <div class="explicacion">
        <v-card class="mb-5">
          <v-card-text>
            <p>
              In this section, you can compare RNA secondary structures to see how similar they are to each other.
              RNA has a structure that can be represented using a special notation called
              <strong>dot-bracket</strong>, where base pairs are represented by parentheses and unpaired bases by dots.
            </p>

            <v-divider class="my-4"></v-divider>

            <h3>1. Enter the RNA sequences</h3>
            <p>
              You need to enter two RNA sequences in <strong>dot-bracket</strong> format. Make sure they don't have
              spaces.
            </p>

            <h3>2. Example sequences:</h3>
            <p class="example-sequences">
              ..((((...))))..<br>
              ..((...))..
            </p>

            <p>
              Each RNA sequence must be in <strong>dot-bracket</strong> format, where dots <code>.</code>
              represent unpaired bases and parentheses <code>()</code> represent paired bases.
            </p>

            <h3>3. Compare the sequences</h3>
            <p>
              The system will analyze the structures and calculate a score indicating how similar they are to each
              other.
              The lower the score, the more similar the structures are.
            </p>
          </v-card-text>
        </v-card>

        <button @click="addExample" class="example-btn">Add Example Sequences</button>
      </div>

      <!-- Sequence Input Section -->
      <div class="sec-sequencias">
        <textarea v-model="secuencia1" placeholder="Enter the first sequence"></textarea>
        <textarea v-model="secuencia2" placeholder="Enter the second sequence"></textarea>
      </div>

      <button @click="compareRNA" :disabled="loading" class="btn-comparar">
        {{ loading ? "Comparing..." : "Compare" }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { VCard, VCardText, VDivider } from 'vuetify/components'

const secuencia1 = ref('')
const secuencia2 = ref('')
const loading = ref(false)
const error = ref(null)
const router = useRouter()

async function compareRNA() {
  try {
    const response = await fetch('/compare', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        structure1: secuencia1.value,
        structure2: secuencia2.value,
      })
    })
    if (!response.ok) throw new Error(`Error HTTP: ${response.status}`)

    const data = await response.json()
    if (data.job_id) {
      // Redirige a la página de status del job y pasa query params para mostrar después
      router.push({
        name: 'JobStatus',
        params: { jobId: data.job_id },
        query: { structure1: secuencia1.value, structure2: secuencia2.value }
      })
    } else {
      throw new Error('No se recibió job_id')
    }
  } catch (error) {
    console.error('Error comparing:', error)
    // Aquí muestra tu mensaje de error en rojo o lo que uses
  }
}

const addExample = () => {
  secuencia1.value = '..((((...))))..'
  secuencia2.value = '..((...))..'
}
</script>