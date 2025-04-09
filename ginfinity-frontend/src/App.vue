<template>
  <div>
    <Header />
    <router-view />
    <ScrollToTop />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Header from './components/Header.vue';
import ScrollToTop from './components/ScrollToTop.vue';


export default defineComponent({
  name: 'App',
  components: {
    Header,
    ScrollToTop,
  },
});
</script>

<style>
* {
  font-family: "Helvetica Neue";
}
</style>
