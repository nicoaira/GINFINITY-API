<template>
    <div class="help-container">
        <section v-for="(section, index) in sections" :key="index" class="help-section">
            <h2 class="section-title">{{ section.title }}</h2>

            <v-card v-for="(entry, i) in section.entries" :key="i" class="faq-card" @click="toggle(section.title, i)"
                :class="{ open: entry.open }">
                <v-card-text class="faq-question">
                    <div class="question-content">
                        {{ entry.question }}
                        <img src="@/components/icons/arrow.svg" alt="Toggle Arrow" class="arrow-icon"
                            :class="{ rotated: entry.open }" />
                    </div>
                </v-card-text>

                <transition name="fade">
                    <div v-if="entry.open" class="faq-answer">
                        {{ entry.answer }}
                    </div>
                </transition>
            </v-card>
        </section>
    </div>
</template>

<script setup>
import { reactive } from 'vue'
import { VCard, VCardText } from 'vuetify/components'

const sections = reactive([
    {
        title: 'General Questions',
        entries: [
            { question: 'Lorem ipsum', answer: 'Lorem ipsum dolor sit amet.', open: false },
            { question: 'Lorem ipsum dolor sit amet consectetur adipisicing elit. ', answer: 'Lorem ipsum dolor sit amet.', open: false }
        ]
    },
    {
        title: 'FAQs',
        entries: [
            { question: 'Molestiae ducimus odit mollitia ipsa,', answer: 'Lorem ipsum dolor sit amet.', open: false },
            { question: 'Dignissimos quasi voluptates perspiciatis ', answer: 'Lorem ipsum dolor sit amet.', open: false }
        ]
    },
    {
        title: 'Tree Processing',
        entries: [
            { question: 'Tree processing', answer: 'Lorem ipsum dolor sit amet.', open: false },
            { question: 'Speciation/duplication detection', answer: 'Lorem ipsum dolor sit amet.', open: false },
            { question: 'Computing meta-homologs', answer: 'Lorem ipsum dolor sit amet.', open: false }
        ]
    },
    {
        title: 'Scoring',
        entries: [
            { question: 'Consistency score', answer: 'Lorem ipsum dolor sit amet.', open: false },
            { question: 'Evidence level', answer: 'Lorem ipsum dolor sit amet.', open: false }
        ]
    }
])

function toggle(sectionTitle, index) {
    const section = sections.find(s => s.title === sectionTitle)
    if (section) section.entries[index].open = !section.entries[index].open
}
</script>