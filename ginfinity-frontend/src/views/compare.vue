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

const compareRNA = async () => {
  if (!secuencia1.value || !secuencia2.value) {
    error.value = 'Please enter both sequences.'
    return
  }

  error.value = null
  loading.value = true

  try {
    const response = await axios.post('/compare', {
      structure1: secuencia1.value,
      structure2: secuencia2.value,
      metric: 'squared',
    })

    router.push({
      name: 'results',
      query: {
        structure1: secuencia1.value,
        structure2: secuencia2.value,
        score: response.data.similarity_score.toString()
      }
    })
  } catch (err) {
    error.value = 'There was an error comparing the sequences.'
  } finally {
    loading.value = false
  }
}

const addExample = () => {
  secuencia1.value = '..((((...))))..'
  secuencia2.value = '..((...))..'
}
</script>