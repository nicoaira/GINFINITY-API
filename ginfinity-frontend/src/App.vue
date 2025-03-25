<template>
  <router-view></router-view>  <!-- Aquí se renderizan las vistas -->
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'App',
});
</script>

<style>
*{
      font-family: "Helvetica Neue";
}
</style>
