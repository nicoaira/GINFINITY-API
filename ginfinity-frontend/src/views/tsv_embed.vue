<template>
  <div class="tsv-uploader">
    <input type="file" @change="handleFileUpload" accept=".tsv" />
    <button @click="processFile" :disabled="!file">Subir archivo</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const file = ref(null);

const handleFileUpload = (event) => {
  const selectedFile = event.target.files[0];
  if (selectedFile && selectedFile.name.endsWith(".tsv")) {
    file.value = selectedFile;
  } else {
    alert("Por favor, selecciona un archivo .tsv válido.");
    file.value = null;
  }
};

const processFile = async () => {
  if (!file.value) return;

  try {
    // Step 1: Send the file to the batch_embed endpoint
    const formData = new FormData();
    formData.append('file', file.value);
    
    const batchResponse = await axios.post("http://localhost:8000/tsv_embed", formData, {
  headers: {
    "Content-Type": "multipart/form-data",
  }
});


    // Step 2: Get the embeddings from the response and add them to the original file
    const embeddings = batchResponse.data.embeddings;  // This assumes the response is an array of embeddings.
    
    const reader = new FileReader();
    reader.onload = async () => {
      const tsvData = reader.result;
      const rows = tsvData.split('\n');
      const header = rows[0].split('\t');
      const idIndex = header.indexOf('id');
      const structureIndex = header.indexOf('secondary_structure');

      if (idIndex === -1 || structureIndex === -1) {
        alert("El archivo debe tener las columnas 'id' y 'secondary_structure'.");
        return;
      }

      // Add embeddings to the TSV data
      const updatedRows = rows.map((row, index) => {
        if (index === 0) {
          return row + '\tembedding_vector'; // Add the new header for embedding
        }

        const columns = row.split('\t');
        const id = columns[idIndex];

        // Find the corresponding embedding
        const embedding = embeddings.find((emb) => emb.id === id);
        if (embedding) {
          columns.push(embedding.embedding);
        } else {
          columns.push(''); // Empty if no embedding found
        }
        return columns.join('\t');
      });

      // Step 3: Log the updated TSV content to the console
      const updatedTsvData = updatedRows.join('\n');
      console.log(updatedTsvData);
    };
    reader.readAsText(file.value);
  } catch (error) {
    console.error('Error al procesar el archivo:', error);
    alert("Hubo un error al procesar el archivo.");
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

input[type="email"] {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  max-width: 300px;
}
</style>
