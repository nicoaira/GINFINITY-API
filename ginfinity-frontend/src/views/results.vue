<template>
    <div class="resultados">
        <v-card class="result-card">
            <v-card-title class="title">
                <h2>{{ pageTitle }}</h2>
            </v-card-title>

            <v-card-text>
                <div v-if="isCompare">
                    <div class="result-item">
                        <strong>Structure 1:</strong>
                        <p class="structure">{{ structure1 }}</p>
                    </div>

                    <div class="result-item">
                        <strong>Structure 2:</strong>
                        <p class="structure">{{ structure2 }}</p>
                    </div>

                    <div class="result-item score-item">
                        <strong>Similarity Score:</strong>
                        <p :class="scoreClass">{{ score }}</p>
                    </div>
                </div>

                <div v-else-if="isTsvEmbed">
                    <div class="result-item">
                        <table v-if="tsvData.length" class="tsv-table">
                            <thead>
                                <tr>
                                    <th v-for="(header, index) in tsvHeaders" :key="index">{{ header }}</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(row, index) in tsvData" :key="index">
                                    <td v-for="(value, idx) in row" :key="idx">{{ value }}</td>
                                </tr>
                            </tbody>
                        </table>
                        <p v-else>No data available in the uploaded TSV file.</p>
                    </div>

                    <v-btn @click="downloadEmbeddedFile" color="success" class="download-btn">
                        Download Resulting TSV
                    </v-btn>
                    <v-card-actions class="buttons-container">
                        <v-btn color="primary" @click="goBack" class="back-btn">Go Back</v-btn>
                    </v-card-actions>
                </div>

                <div v-else>
                    <p>No results available for this request.</p>
                </div>
            </v-card-text>
        </v-card>
    </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { ref } from 'vue'

const route = useRoute()
const router = useRouter()

const requestType = route.query.requestType ? String(route.query.requestType) : 'compare'

const structure1 = route.query.structure1 ? String(route.query.structure1) : 'Not available'
const structure2 = route.query.structure2 ? String(route.query.structure2) : 'Not available'
const score = route.query.score ? String(route.query.score) : 'Not calculated'
const scoreClass = score === 'Not calculated' ? 'no-score' : 'score'

const isCompare = requestType === 'compare'
const isTsvEmbed = requestType === 'tsv_embed'

const pageTitle = isCompare ? 'Comparison Result' : isTsvEmbed ? 'Embedding Result' : 'Results'

// Leemos el TSV embebido de sessionStorage y parseamos los datos
const tsvEmbedResult = ref<string | null>(null)
const tsvData = ref<Array<Array<string>>>([]) // Datos del TSV
const tsvHeaders = ref<Array<string>>([]) // Encabezados del TSV

if (isTsvEmbed) {
    const savedText = sessionStorage.getItem('tsvEmbedText')
    tsvEmbedResult.value = savedText || 'No TSV result found.'

    // Parseamos el contenido TSV
    if (tsvEmbedResult.value) {
        const lines = tsvEmbedResult.value.split('\n')
        tsvHeaders.value = lines[0].split('\t')
        tsvData.value = lines.slice(1).map(line => line.split('\t'))
    }
}

const goBack = () => {
    router.go(-1)
}

const downloadEmbeddedFile = () => {
    if (!tsvEmbedResult.value) return
    const blob = new Blob([tsvEmbedResult.value], { type: 'text/tab-separated-values' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'embedded_result.tsv'
    link.click()
}
</script>
