<template>
  <div class="tsv-uploader">
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

    <h2 class="embed-title">Cálculo de Embeddings para Estructuras Secundarias de ARN</h2>

    <div class="explicacion">
      <v-card class="mb-5">
        <v-card-text>
          <p>
            En esta sección, puedes cargar un archivo TSV que contenga al menos dos columnas: <strong>id</strong> y
            <strong>secondary_structure</strong>.
            El sistema calculará un embedding para cada estructura secundaria de ARN contenida en la columna
            <strong>secondary_structure</strong>.
          </p>

          <v-divider class="my-4"></v-divider>

          <h3>1. Subir el archivo TSV</h3>
          <p>
            Para usar este servicio, primero debes subir un archivo TSV que contenga las columnas <strong>id</strong> y
            <strong>secondary_structure</strong>.
            Asegúrate de que el archivo esté bien formateado y que las columnas tengan los nombres correctos.
          </p>

          <h3>2. Ejemplo de archivo TSV:</h3>
          <p class="example-sequences">
            id secondary_structure<br>
            seq1 ..((((...))))..<br>
            seq2 ..((...))..
          </p>

          <p>
            Cada fila debe contener un identificador único en la columna <strong>id</strong> y una estructura secundaria
            de ARN en formato <strong>dot-bracket</strong>
            en la columna <strong>secondary_structure</strong>.
          </p>

          <h3>3. Proceso de cálculo de embeddings</h3>
          <p>
            El sistema procesará el archivo, calculará un embedding para cada estructura secundaria y agregará una nueva
            columna <strong>embedding_vector</strong> al archivo original.
            El archivo resultante estará listo para descargar.
          </p>

          <h3>4. Descargar el archivo actualizado</h3>
          <p>
            Después de procesar el archivo, podrás descargar el archivo con los embeddings generados.
          </p>
        </v-card-text>
      </v-card>

      <button class="example-btn" @click="downloadExampleFile">
        Descargar archivo de ejemplo
      </button>
    </div>

    <div class="tsv-content">
      <v-card class="upload-card">
        <v-card-title>
          <h3>Subir archivo TSV</h3>
        </v-card-title>

        <v-card-text>

          <v-file-input v-model="file" label="Selecciona o arrastra un archivo TSV" accept=".tsv" outlined
            @change="handleFileUpload"></v-file-input>
        </v-card-text>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <v-row>
          <v-col>
            <v-btn @click="processFile" :disabled="!file" class="upload-btn" block>
              Subir archivo
            </v-btn>
          </v-col>
        </v-row>

        <v-row justify="center" text-align="center">
          <v-col cols="12" md="8">
            <v-btn v-if="downloadUrl" :href="downloadUrl" download="updated_file.tsv" class="download-btn" block>
              Descargar archivo actualizado
            </v-btn>
          </v-col>
        </v-row>
      </v-card>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { VCard, VCardText, VFileInput, VContainer, VRow, VBtn, VCardTitle, VCol, VDivider } from 'vuetify/components';

const file = ref(null);
const downloadUrl = ref(null);
const errorMessage = ref(null);
let previousFileData = null; 

const handleFileUpload = (event) => {
  const uploadedFile = event.target.files[0];

  downloadUrl.value = null; 
  errorMessage.value = null;

  if (uploadedFile && uploadedFile.name.endsWith('.tsv')) {
    file.value = uploadedFile;

    const reader = new FileReader();
    reader.onload = (e) => {
      const content = e.target.result;
      const rows = content.split('\n');
      const header = rows[0].split('\t'); 

      if (previousFileData && previousFileData !== content) {
        errorMessage.value = 'Las secuencias han cambiado. Se actualizarán los embeddings.';
      }

      previousFileData = content;
    };
    reader.readAsText(uploadedFile);
  } else {
    errorMessage.value = 'Por favor, sube un archivo TSV válido.';
    file.value = null;
  }
};

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
      if (response.status === 400) { 
        errorMessage.value = 'El formato del archivo no es válido. Por favor, revisa el archivo y vuelve a intentarlo.';
      } else {
        throw new Error('Error al procesar el archivo.');
      }
      return;
    }

    const updatedFile = await response.blob();
    downloadUrl.value = URL.createObjectURL(updatedFile);
  } catch (error) {
    console.error('Error al procesar el archivo:', error);
  }
};

const downloadExampleFile = () => {
  const exampleData = `id\tsecondary_structure\nseq1\t..((((...))))..\nseq2\t..((...))..`;
  const blob = new Blob([exampleData], { type: 'text/tab-separated-values' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'example_file.tsv';
  link.click();
};
</script>