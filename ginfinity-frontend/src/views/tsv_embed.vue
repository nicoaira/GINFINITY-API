<template>
  <div class="tsv-uploader">
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

    <h2 class="embed-title">Embedding Calculation for RNA Secondary Structures</h2>

    <div class="explicacion">
      <v-card class="mb-5">
        <v-card-text>
          <p>
            In this section, you can upload a TSV file containing at least two columns: <strong>id</strong> and
            <strong>secondary_structure</strong>.
            The system will calculate an embedding for each RNA secondary structure contained in the <strong>secondary_structure</strong> column.
          </p>

          <v-divider class="my-4"></v-divider>

          <h3>1. Upload the TSV file</h3>
          <p>
            To use this service, you must first upload a TSV file containing the <strong>id</strong> and
            <strong>secondary_structure</strong> columns.
            Make sure the file is properly formatted and the columns have the correct names.
          </p>

          <h3>2. Example of a TSV file:</h3>
          <p class="example-sequences">
            id secondary_structure<br>
            seq1 ..((((...))))..<br>
            seq2 ..((...))..
          </p>

          <p>
            Each row should contain a unique identifier in the <strong>id</strong> column and an RNA secondary structure
            in <strong>dot-bracket</strong> format in the <strong>secondary_structure</strong> column.
          </p>

          <h3>3. Embedding calculation process</h3>
          <p>
            The system will process the file, calculate an embedding for each secondary structure, and add a new
            <strong>embedding_vector</strong> column to the original file.
            The resulting file will be ready for download.
          </p>

          <h3>4. Download the updated file</h3>
          <p>
            After processing the file, you will be able to download the file with the generated embeddings.
          </p>
        </v-card-text>
      </v-card>

      <button class="example-btn" @click="downloadExampleFile">
        Download Example File
      </button>
    </div>

    <div class="tsv-content">
      <v-card class="upload-card">
        <v-card-title class="upload-card-title">
          <h3>Upload TSV File</h3>
        </v-card-title>

        <v-card-text>

          <v-file-input v-model="file" label="Select or drag a TSV file" accept=".tsv" outlined class="file-input"
            @change="handleFileUpload"></v-file-input>
        </v-card-text>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <v-row>
          <v-col>
            <v-btn @click="processFile" :disabled="!file" class="upload-btn" block>
              Upload File
            </v-btn>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-btn v-if="downloadUrl" :href="downloadUrl" download="updated_file.tsv" class="download-btn" block>
              Download Updated File
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
        errorMessage.value = '';
      }

      previousFileData = content;
    };
    reader.readAsText(uploadedFile);
  } else {
    errorMessage.value = 'Please upload a valid TSV file.';
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
        errorMessage.value = 'The file format is invalid. Please check the file and try again.';
      } else {
        throw new Error('Error processing the file.');
      }
      return;
    }

    const updatedFile = await response.blob();
    downloadUrl.value = URL.createObjectURL(updatedFile);
  } catch (error) {
    console.error('Error processing the file:', error);
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
