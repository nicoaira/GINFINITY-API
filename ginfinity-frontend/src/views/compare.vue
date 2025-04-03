<template>
  <div class="comparador">
    <!-- Header -->
    <header class="header">
      <div class="logo">
        <router-link to="/">
          <img src="@/assets/logo.png" alt="Ginfinity Logo" />
        </router-link>
      </div>
      <nav class="navbar">
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/comparar-arn">Compare Sequences</router-link></li>
          <li><router-link to="/calcular-embeddings">Calculate Embeddings</router-link></li>
        </ul>
      </nav>
    </header>

    <!-- Comparador Section -->
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
              You need to enter two RNA sequences in <strong>dot-bracket</strong> format. Make sure they don't have spaces.
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
              The system will analyze the structures and calculate a score indicating how similar they are to each other.
              The lower the score, the more similar the structures are.
            </p>
          </v-card-text>
        </v-card>

        <!-- Button to add example sequence -->
        <button @click="addExample" class="example-btn">Add Example Sequences</button>
      </div>

      <!-- Form to compare sequences -->
      <div class="sec-sequencias">
        <textarea v-model="secuencia1" placeholder="Enter the first sequence"></textarea>
        <textarea v-model="secuencia2" placeholder="Enter the second sequence"></textarea>
      </div>
      <button @click="compareRNA" :disabled="loading" class="btn-comparar">
        {{ loading ? "Comparing..." : "Compare" }}
      </button>

      <!-- Comparison result aligned to the left -->
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="result !== null" class="compare-result">{{ `Similarity: ${result}` }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { VCard, VCardText, VDivider } from 'vuetify/components'

const secuencia1 = ref('')
const secuencia2 = ref('')
const result = ref(null)
const loading = ref(false)
const error = ref(null)

const compareRNA = async () => {
  if (!secuencia1.value || !secuencia2.value) {
    error.value = 'Please enter both sequences.'
    return
  }

  error.value = null
  loading.value = true
  result.value = null

  const config = {
    headers: {
      'Content-Type': 'application/json',
    }
  }

  try {
    const response = await axios.post('/compare', {
      structure1: secuencia1.value,
      structure2: secuencia2.value,
      metric: 'squared',
    }, config);
    result.value = response.data.similarity_score;
  } catch (err) {
    error.value = 'There was an error comparing the sequences.';
  } finally {
    loading.value = false;
  }
}

// Function to add an example sequence
const addExample = () => {
  secuencia1.value = '..((((...))))..';
  secuencia2.value = '..((...))..';
}
</script>
