<template>
  <div class="comparador">
    <!-- Header -->
    <header class="header">
      <div class="logo">
        <img src="@/assets/logo.png" alt="Ginfinity Logo" />
      </div>
      <nav class="navbar">
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/comparar-arn">Compare Sequences</router-link></li>
          <li><router-link to="/calcular-embeddings">Calcule Embeddings</router-link></li>
        </ul>
      </nav>
    </header>

    <!-- Comparador Section -->
    <div class="comparador-content">
      <h2 class="compare-title">Comparador Secuencias de ARN</h2>

      <!-- Sección Explicativa -->
      <div class="explicacion">
        <v-card class="mb-5">
          <v-card-text>
            <p>
              En esta sección, puedes comparar las estructuras secundarias de ARN para ver qué tan similares son entre
              sí. El ARN tiene una estructura que se puede representar mediante una notación especial llamada
              <strong>dot-bracket</strong>, donde los pares de bases están representados por paréntesis y las bases no
              emparejadas por puntos.
            </p>

            <v-divider class="my-4"></v-divider>

            <h3>1. Introduce las secuencias de ARN</h3>
            <p>
              Tienes que ingresar dos secuencias de ARN en formato <strong>dot-bracket</strong>. Asegúrate de que no
              tengan espacios.
            </p>

            <h3>2. Ejemplo de secuencias:</h3>
            <p class="example-sequences">
              ..((((...))))..<br>
              ..((...))..
            </p>

            <p>
              Cada secuencia de ARN debe estar en formato <strong>dot-bracket</strong>, que usa puntos <code>.</code>
              para representar bases no emparejadas y paréntesis <code>()</code> para las bases que están emparejadas.
            </p>

            <h3>3. Compara las secuencias</h3>
            <p>
              El sistema analizará las estructuras y calculará una puntuación que indica cuán similares son entre sí.
              Cuanto más baja sea la puntuación, más similares son las estructuras.
            </p>
          </v-card-text>
        </v-card>

        <!-- Botón para añadir una secuencia de ejemplo -->
          <button @click="añadirEjemplo" class="example-btn">Añadir Secuencias de Ejemplo</button>
      </div>

      <!-- Formulario para comparar secuencias -->
      <div class="sec-sequencias">
        <textarea v-model="secuencia1" placeholder="Introduce la primera secuencia"></textarea>
        <textarea v-model="secuencia2" placeholder="Introduce la segunda secuencia"></textarea>
      </div>
      <button @click="compararARN" :disabled="cargando" class="btn-comparar">
        {{ cargando ? "Comparando..." : "Comparar" }}
      </button>

      <!-- Resultado de la comparación alineado a la izquierda -->
      <p v-if="error" class="error">{{ error }}</p>
      <p v-if="resultado !== null" class="compare-result">{{ `Similitud: ${resultado}` }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { VCard, VCardText, VDivider } from 'vuetify/components'

const secuencia1 = ref('')
const secuencia2 = ref('')
const resultado = ref(null)
const cargando = ref(false)
const error = ref(null)

const compararARN = async () => {
  if (!secuencia1.value || !secuencia2.value) {
    error.value = 'Por favor, introduce ambas secuencias.'
    return
  }

  error.value = null
  cargando.value = true
  resultado.value = null

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
    resultado.value = response.data.similarity_score;
  } catch (err) {
    error.value = 'Hubo un error al comparar las secuencias.';
  } finally {
    cargando.value = false;
  }
}

// Función para añadir un ejemplo de secuencia
const añadirEjemplo = () => {
  secuencia1.value = '..((((...))))..';
  secuencia2.value = '..((...))..';
}
</script>
