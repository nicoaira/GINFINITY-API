<template>
    <button class="scroll-to-top" @click="scrollToTop" v-show="isVisible">
        <img src="@/components/icons/ScrollToTop.svg" alt="Scroll to Top" />
    </button>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)

const toggleVisibility = () => {
    isVisible.value = window.scrollY > 200
}

const scrollToTop = () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth',
    })
}

onMounted(() => {
    window.addEventListener('scroll', toggleVisibility)
})

onUnmounted(() => {
    window.removeEventListener('scroll', toggleVisibility)
})
</script>

<style scoped>

</style>