<template>
  <div class="embedding">
    <!-- Header -->
    <header class="header">
      <div class="logo">
        <img src="@/assets/logo.png" alt="Ginfinity Logo" />
      </div>
      <nav class="navbar">
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/comparar-arn">Compare Sequences</router-link></li>
          <li><router-link to="/embedding-arn">Embeddings</router-link></li>
        </ul>
      </nav>
    </header>

    <!-- Embedding Section -->
    <div class="embedding-content">
      <h2>Obtener Embedding de ARN</h2>

      <!-- Sección Explicativa -->
      <div class="explicacion">
        <v-card class="mb-5">
          <v-card-text>
            <p>
              En esta sección, puedes obtener una representación numérica (embedding) de la secuencia estructural de ARN que introduzcas.
              La notación debe ser en formato <strong>dot-bracket</strong>. Asegúrate de que no tenga espacios.
            </p>

            <v-divider class="my-4"></v-divider>

            <h3>¿Cómo se calcula el embedding?</h3>
            <p>
              El embedding de ARN se calcula mediante un modelo entrenado que transforma la estructura secundaria del ARN (en formato dot-bracket)
              en un vector numérico. El modelo captura características relevantes de la estructura del ARN, como los patrones de emparejamiento
              de bases y la organización general de la secuencia. Este vector numérico puede ser utilizado para tareas de análisis, como la comparación
              de secuencias de ARN o la predicción de propiedades biológicas.
            </p>

            <h3>Ejemplo de secuencia:</h3>
            <p class="example-sequence">
              ..((((...))))..<br>
              ..((...))..
            </p>

            <p>
              Cada secuencia de ARN debe estar en formato <strong>dot-bracket</strong>, que usa puntos <code>.</code>
              para representar bases no emparejadas y paréntesis <code>()</code> para las bases que están emparejadas.
            </p>

            <h3>Proceso:</h3>
            <p>
              En esta sección, puedes introducir la estructura secundaria del ARN para obtener el embedding correspondiente.
            </p>
          </v-card-text>
        </v-card>
      </div>

      <!-- Formulario para obtener el embedding -->
      <div class="sec-sequencia">
        <textarea v-model="secuencia" placeholder="Introduce la secuencia de ARN"></textarea>
      </div>
      <button @click="obtenerEmbedding" :disabled="cargando">
        {{ cargando ? "Obteniendo embedding..." : "Obtener Embedding" }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
      <div v-if="embedding.length > 0" class="resultado">
        <p><strong>Embedding:</strong></p>
        <div class="embedding-scroll">
          <div v-for="(valor, index) in embedding" :key="index" class="embedding-value">
            {{ valor }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const secuencia = ref('')
const embedding = ref([]) // Asegúrate de que sea un array vacío por defecto
const cargando = ref(false)
const error = ref(null)

const obtenerEmbedding = async () => {
  if (!secuencia.value) {
    error.value = 'Por favor, introduce una secuencia de ARN.'
    return
  }

  error.value = null
  cargando.value = true
  embedding.value = [] // Reinicia el array antes de obtener los nuevos datos

  const config = {
    headers: {
      'Content-Type': 'application/json',
    }
  }

  try {
    const response = await axios.post('/embed', {
      structure: secuencia.value,
    }, config);
    
    if (response.data && Array.isArray(response.data.embedding)) {
      embedding.value = response.data.embedding;
    } else {
      error.value = 'No se recibió el embedding de ARN.';
    }
  } catch (err) {
    error.value = 'Hubo un error al obtener el embedding.';
  } finally {
    cargando.value = false;
  }
}
</script>


<style scoped>
.embedding {
  padding: 40px;
  background-color: #ffffff;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 900px;
  margin: 0 auto;
}

.embedding-content {
  text-align: center;
  margin-top: 60px;
}

h2 {
  font-size: 2rem;
  color: #007bff;
  margin-bottom: 20px;
  font-weight: bold;
}

.sec-sequencia {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

textarea {
  width: 280px;
  height: 80px;
  padding: 15px;
  border: 2px solid #007bff;
  border-radius: 10px;
  font-size: 16px;
  resize: none;
  transition: all 0.3s ease;
}

textarea:focus {
  outline: none;
  border-color: #0056b3;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.5);
}

button {
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

button:hover {
  background-color: #0056b3;
  transform: scale(1.05);
}

button:disabled {
  background-color: #b0c4de;
  cursor: not-allowed;
  transform: none;
}

.error {
  color: #d9534f;
  font-weight: bold;
  margin-top: 15px;
}

.resultado {
  font-size: 20px;
  font-weight: bold;
  color: black;
  margin-top: 20px;
}

.embedding-scroll {
  max-height: 200px;
  overflow-y: auto;
  margin-top: 10px;
}

.embedding-value {
  font-size: 14px;
  color: #333;
  margin: 5px 0;
  padding: 5px;
  background-color: #f5f5f5;
  border-radius: 5px;
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

.navbar ul li a.active {
  color: #ffb800;
}

/* Estilo para el bloque de texto de las secuencias */
.example-sequence {
  display: inline-block;
  text-align: center;
  font-size: 1.2rem;
  white-space: pre-wrap;
  word-wrap: break-word;
  margin: 0 auto;
}
</style>
