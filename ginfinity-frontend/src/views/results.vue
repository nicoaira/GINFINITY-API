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
                        <strong>Embedding Result:</strong>
                        <p class="embedding-result">{{ tsvEmbedResult }}</p>
                    </div>
                </div>

                <div v-else>
                    <p>No results available for this request.</p>
                </div>
            </v-card-text>

            <v-card-actions>
                <v-btn color="primary" @click="goBack" class="back-btn">
                    Go Back
                </v-btn>
            </v-card-actions>
        </v-card>
    </div>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const requestType = route.query.requestType ? String(route.query.requestType) : 'compare'

const structure1 = route.query.structure1 ? String(route.query.structure1) : 'Not available'
const structure2 = route.query.structure2 ? String(route.query.structure2) : 'Not available'
const score = route.query.score ? String(route.query.score) : 'Not calculated'
const scoreClass = score === 'Not calculated' ? 'no-score' : 'score'

const tsvEmbedResult = route.query.tsvEmbedResult ? String(route.query.tsvEmbedResult) : 'Not available'

const isCompare = requestType === 'compare'
const isTsvEmbed = requestType === 'tsv_embed'

const pageTitle = isCompare ? 'Comparison Result' : isTsvEmbed ? 'Embedding Result' : 'Results'

const goBack = () => {
  router.go(-1)
}
</script>
