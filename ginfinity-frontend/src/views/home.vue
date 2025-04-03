<template>
  <div class="home-view">
    <!-- Header -->
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
          <li><router-link to="/calcular-embeddings">Calcule Embeddings</router-link></li>
        </ul>
      </nav>
    </header>

    <!-- Hero Section with Image -->
    <section class="section section--bg">
      <div class="hero-content">
        <h1>Computational RNA Biology</h1>
        <h2>Research Group</h2>
        <p>
          Exploring RNA functions and evolution through computational approaches.
        </p>
      </div>
    </section>

    <!-- GinfinityTools Section -->
    <section class="ginfinitytools">
      <h3>What GinfinityTools Can Do</h3>
      <div class="ginfinitytools-content">
        <p>
          GinfinityTools is a suite of tools designed to facilitate the exploration of RNA secondary structures. By leveraging Graph Isomorphism Networks (GIN), we generate embeddings from RNA structures that can be used for a variety of downstream tasks such as clustering, classification, and more. With our tools, users can:
        </p>
        <div class="tools-cards">
          <div class="card">
            <h4>Generate Embeddings</h4>
            <p>Generate embeddings from RNA secondary structures using GIN.</p>
          </div>
          <div class="card">
            <h4>Visualize with t-SNE</h4>
            <p>Visualize embeddings with t-SNE for a deeper understanding of RNA data.</p>
          </div>
          <div class="card">
            <h4>Compare Sequences</h4>
            <p>Compare RNA sequences to identify structural similarities.</p>
          </div>
          <div class="card">
            <h4>Find Structural Orthologs</h4>
            <p>Find structural orthologs across different RNA sequences.</p>
          </div>
          <div class="card">
            <h4>Cluster and Classify</h4>
            <p>Analyze RNA data for clustering and classification tasks.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- About Section with Image -->
    <section class="about">
      <h3>About the Group</h3> 
      <div class="about-content">
        <div class="text">
          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque et dictum urna. Donec et magna nec magna rutrum bibendum. Integer tincidunt metus non gravida egestas. Nulla facilisi. Fusce sagittis eros neque, a faucibus nunc blandit at.
          </p>
        </div>
        <div class="image">
          <img src="https://via.placeholder.com/500x350" alt="About Image" />
        </div>
      </div>
    </section>

    <!-- Publications Section with Images -->
    <section class="publications">
      <h3>Publications and Projects</h3>
      <div class="card-container">
        <div class="card">
          <img src="https://via.placeholder.com/350x200" alt="Publication 1" />
          <h4>Publication 1</h4>
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
        </div>
        <div class="card">
          <img src="https://via.placeholder.com/350x200" alt="Publication 2" />
          <h4>Publication 2</h4>
          <p>Nulla facilisi. Fusce sagittis eros neque, a faucibus nunc blandit at.</p>
        </div>
        <div class="card">
          <img src="https://via.placeholder.com/350x200" alt="Publication 3" />
          <h4>Publication 3</h4>
          <p>Integer tincidunt metus non gravida egestas. Curabitur fringilla arcu ac tincidunt hendrerit.</p>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="team">
      <h3>Our Team</h3>
      <div class="team-members">
        <div class="team-member">
          <img src="@/assets/perfil.png" alt="Team Member 1" />
          <h4>Dr. John Doe</h4>
          <p>Lead Researcher</p>
        </div>
        <div class="team-member">
          <img src="@/assets/perfil.png" alt="Team Member 2" />
          <h4>Dr. Jane Smith</h4>
          <p>RNA Specialist</p>
        </div>
        <div class="team-member">
          <img src="@/assets/perfil.png" alt="Team Member 3" />
          <h4>Dr. Alice Brown</h4>
          <p>Bioinformatics Expert</p>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <p>© 2025 Universitat Internacional de Catalunya</p>
      <p>
        Legal advice
        Cookies Policy | 
        Privacy and data protection
      </p>
      <p>
        Contact
        Work at UIC Barcelona
      </p>
    </footer>
  </div>
</template>

<script lang="ts">
export default {
  name: "HomeView",
};
</script>
