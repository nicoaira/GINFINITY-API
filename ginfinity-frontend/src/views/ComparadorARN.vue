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
          <li><router-link to="/calcular-embeddings">Compare Embeddings</router-link></li>
        </ul>
      </nav>
    </header>

    <!-- Comparador Section -->
    <div class="comparador-content">
      <h2>Comparar Secuencias de ARN</h2>

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
        <div class="boton-ejemplo">
          <button @click="añadirEjemplo" class="btn-ejemplo">Añadir Secuencias de Ejemplo</button>
        </div>
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
      <p v-if="resultado !== null" class="resultado">{{ `Similitud: ${resultado}` }}</p>
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

<style scoped>
.comparador {
  padding: 40px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.comparador-content {
  margin-top: 60px;
  text-align: left;  /* Cambié a izquierda */
}

h2 {
  font-size: 2rem;
  color: black;
  margin-bottom: 20px;
  font-weight: bold;
}

/* Alineación del formulario a la izquierda */
.sec-sequencias {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

textarea {
  width: 100%;
  max-width: 600px;
  height: 80px;
  padding: 15px;
  border: 2px solid black;
  border-radius: 10px;
  font-size: 16px;
  resize: none;
  transition: all 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: black;
}

.btn-comparar {
  align-self: flex-start;  /* Alineación izquierda */
  padding: 14px 30px;
  font-size: 15px;
  font-weight: bold;
  color: white;
  background-color: #007bff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-comparar:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

.btn-comparar:disabled {
  background-color: #b0c4de;
  cursor: not-allowed;
  transform: none;
}

/* Alineación del resultado a la izquierda */
.resultado {
  font-size: 20px;
  font-weight: bold;
  color: black;
  margin-top: 20px;
  text-align: left;  /* Alineación izquierda */
}

.error {
  color: #d9534f;
  font-weight: bold;
  margin-top: 15px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #049bdc;
  color: white;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 60px;
}

.header .logo img {
  height: 60px;
}

.navbar ul {
  display: flex;
  list-style: none;
  gap: 20px;
}

.navbar ul li a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.navbar ul li a:hover {
  text-decoration: underline;
}

/* Estilo para el botón de ejemplo como un link */
.boton-ejemplo {
  text-align: left;
  margin-top: 20px;
}

.boton-ejemplo .btn-ejemplo {
  padding: 0;
  font-size: 16px;
  background-color: transparent;
  color: black;
  border: none;
  text-decoration: underline;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 10px;
}

.boton-ejemplo .btn-ejemplo:hover {
  color: black;
  text-decoration: underline;
}

/* Estilo para el bloque de texto de las secuencias */
.example-sequences {
  display: inline-block;
  text-align: center;
  font-size: 1.2rem;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0 auto;
}
</style>
