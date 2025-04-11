<template>
  <header class="header" :class="{ 'header-hidden': isScrolled }">
    <nav class="navbar">
      <ul class="navbar-list">
        <li class="nav-item" style="--delay: 0s">
          <router-link to="/">Home</router-link>
        </li>
        <li class="nav-item" style="--delay: 0.1s">
          <router-link to="/comparar-arn">Compare Sequences</router-link>
        </li>

        <li class="logo-item">
          <router-link to="/" class="logo-link">
            <img src="@/assets/logo.png" alt="Ginfinity Logo" class="logo-img" />
          </router-link>
        </li>

        <li class="nav-item" style="--delay: 0.2s">
          <router-link to="/calcular-embeddings">Calculate Embeddings</router-link>
        </li>
        <li class="nav-item" style="--delay: 0.3s">
          <router-link to="/help">Help</router-link>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  data() {
    return {
      isScrolled: false,
    };
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    handleScroll() {
      this.isScrolled = window.scrollY > 50;
    },
  },
};
</script>