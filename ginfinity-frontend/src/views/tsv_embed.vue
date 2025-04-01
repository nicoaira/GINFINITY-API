<template>
  <div class="tsv-uploader">
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
    <input type="file" @change="handleFileUpload" accept=".tsv" />
    <button @click="processFile" :disabled="!file">Subir archivo</button>
    <!-- Solo mostrar el enlace de descarga si downloadUrl tiene valor -->
    <a v-if="downloadUrl" :href="downloadUrl" download="updated_file.tsv">
      Descargar archivo actualizado
    </a>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Estado reactivo para almacenar el archivo, el enlace de descarga
const file = ref(null);
const downloadUrl = ref(null);

// Paso 1: Manejar la carga del archivo
const handleFileUpload = (event) => {
  const uploadedFile = event.target.files[0];
  if (uploadedFile && uploadedFile.name.endsWith('.tsv')) {
    file.value = uploadedFile;
  } else {
    alert('Por favor, sube un archivo TSV.');
  }
};

// Paso 2: Subir el archivo al backend para que lo procese y agregue la columna de embeddings
const processFile = async () => {
  if (!file.value) return;

  const formData = new FormData();
  formData.append('file', file.value);

  try {
    const response = await fetch('/tsv_embed', {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error('Error al procesar el archivo.');
    }

    // Paso 3: Recibir el archivo actualizado y generar el enlace para descargarlo
    const updatedFile = await response.blob();
    downloadUrl.value = URL.createObjectURL(updatedFile);
  } catch (error) {
    console.error('Error al procesar el archivo:', error);
  }
};
</script>

<style scoped>
.tsv-uploader {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}

input[type="file"] {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  max-width: 300px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

a {
  margin-top: 10px;
  text-decoration: none;
  color: #0066cc;
}

a:hover {
  text-decoration: underline;
}
</style>
