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
          <li><router-link to="/embedding-arn">Embeddings</router-link></li>
        </ul>
      </nav>
    </header>

    <!-- Comparador Section -->
    <div class="comparador-content">
      <h2>Calcular Embeddings desde un Archivo</h2>

      <!-- Sección Explicativa -->
      <div class="explicacion">
        <v-card class="mb-5">
          <v-card-text>
            <p>
              En esta sección, puedes cargar un archivo CSV o TSV que contenga una columna de estructuras secundarias de ARN. 
              El archivo debe tener un formato con al menos dos columnas: "id" y "secondary_structure".
            </p>
            <v-divider class="my-4"></v-divider>

            <h3>Formato del archivo:</h3>
            <ul>
              <li>Debe contener una columna "id".</li>
              <li>Debe contener una columna "secondary_structure".</li>
            </ul>
            <p>El sistema calculará los embeddings de las estructuras de ARN y devolverá el archivo con una nueva columna de "embeddings".</p>
          </v-card-text>
        </v-card>
      </div>

      <!-- Área de arrastre y suelta -->
      <div 
        class="dropzone" 
        @dragover.prevent
        @drop="handleDrop"
      >
        <p>Arrastra y suelta un archivo CSV o TSV aquí</p>
      </div>

      <!-- Botón para seleccionar archivo -->
      <div class="file-upload">
        <v-file-input 
          v-model="selectedFile" 
          label="Selecciona un archivo CSV o TSV" 
          accept=".csv, .tsv" 
          outlined 
          @change="handleFileChange"
        />
      </div>

      <!-- Botón para subir el archivo -->
      <v-btn v-if="file" @click="uploadFile">Subir archivo</v-btn>

      <!-- Alertas -->
      <v-alert v-if="error" type="error">{{ error }}</v-alert>
      <v-alert v-if="success" type="success">{{ success }}</v-alert>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { VCard, VCardText, VBtn, VFileInput, VAlert, VDivider } from 'vuetify/components';

const selectedFile = ref(null);
const file = ref(null);
const error = ref(null);
const success = ref(null);

const handleDrop = (event) => {
  event.preventDefault();
  const droppedFile = event.dataTransfer.files[0];

  if (!droppedFile) {
    error.value = 'No se detectó ningún archivo.';
    return;
  }

  if (!droppedFile.name.endsWith('.csv') && !droppedFile.name.endsWith('.tsv')) {
    error.value = 'Solo se pueden subir archivos CSV o TSV.';
    file.value = null;
    success.value = null;
    return;
  }

  file.value = droppedFile;
  error.value = null;
  success.value = `Archivo '${droppedFile.name}' listo para subir.`;
  selectedFile.value = null;
};

const handleFileChange = () => {
  if (!selectedFile.value) return;

  if (!selectedFile.value.name.endsWith('.csv') && !selectedFile.value.name.endsWith('.tsv')) {
    error.value = 'Solo se pueden subir archivos CSV o TSV.';
    file.value = null;
    success.value = null;
    return;
  }

  file.value = selectedFile.value;
  error.value = null;
  success.value = `Archivo '${selectedFile.value.name}' listo para subir.`;
};

const uploadFile = async () => {
  if (!file.value) {
    error.value = 'No hay archivo seleccionado.';
    return;
  }

  const formData = new FormData();
  formData.append('file', file.value);

  console.log('Enviando archivo:', file.value.name);
  console.log('FormData:', formData);

  try {
    const response = await axios.post('/embed_from_file', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });

    console.log('Respuesta del servidor:', response.data);
    success.value = 'Archivo subido y procesado correctamente.';
    error.value = null;
  } catch (err) {
    console.error('Error al subir el archivo:', err);
    error.value = 'Hubo un error al procesar el archivo.';
    success.value = null;
  }
};
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
  text-align: left;
}

h2 {
  font-size: 2rem;
  color: black;
  margin-bottom: 20px;
  font-weight: bold;
}

.dropzone {
  border: 2px dashed #007bff;
  border-radius: 10px;
  padding: 30px;
  text-align: center;
  background-color: #f0f8ff;
  margin-top: 20px;
}

.dropzone p {
  font-size: 18px;
  color: #007bff;
}

.file-upload {
  margin-top: 20px;
}

.v-alert {
  margin-top: 20px;
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
</style>
