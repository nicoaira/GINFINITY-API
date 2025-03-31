<template>
  <div class="home-view">
    <!-- Header -->
    <header class="header">
      <div class="logo">
        <img src="@/assets/logo.png" alt="Ginfinity Logo" />
      </div>
      <nav class="navbar">
        <ul>
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/comparar-arn">Compare Sequences</router-link></li>
          <li><router-link to="/calcular-embeddings">Compare Embeddings</router-link></li>
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
      <p>© 2021 Universitat Internacional de Catalunya</p>
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

<style scoped>
.home-view {
  font-family: 'Arial', sans-serif;
  color: #333;
  padding: 0;
  margin: 0;
  height: 100%;
  width: 100%;
  background-color: #f4f6f9; /* Fondo de color gris suave */
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: #049bdc;
  color: white;
  position: fixed; /* Fijar el encabezado */
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: 60px;
}

.header .logo img {
  height: 60px;
}

.navbar ul {
  display: flex;
  list-style: none;
  gap: 20px;
}

.navbar ul li a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

.navbar ul li a:hover {
  text-decoration: underline;
}

.section--bg {
  max-width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-size: 3rem;
  text-align: center;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.4)), url('https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/UIC_Campus_Sant_Cugat.jpg/1200px-UIC_Campus_Sant_Cugat.jpg');
  background-repeat: no-repeat, no-repeat;
  background-size: cover, cover;
  background-position: center, center;
  background-attachment: fixed;
}

.section--bg h1 {
  color: white;  /* Texto blanco para resaltar */
  text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.7);  /* Sombra para el texto */
  font-weight: bold;  /* Hacer el texto más grueso */
  -webkit-background-clip: text;
  background-clip: text;  /* Aplicar el color de fondo solo al texto */
  padding: 10px;
  border-radius: 10px;
}

.hero-content {
  color: white;
}

.hero h1 {
  font-size: 4rem;
  font-weight: bold;
}

.hero h2 {
  font-size: 2rem;
  margin-top: 20px;
}

.hero .button {
  background-color: #007b99;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
  margin-top: 20px;
}

.hero .button:hover {
  background-color: #005f73;
}

.ginfinitytools {
  padding: 40px;
  background-color: #ffffff;
  margin: 20px 0;
}

.ginfinitytools h3 {
  font-size: 2rem;
  margin-bottom: 20px;
}

.ginfinitytools-content ul {
  list-style: none;
  padding-left: 20px;
}

.ginfinitytools-content ul li {
  margin-bottom: 10px;
}

.tools-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  margin-top: 20px;

}

.card {
  background-color: #f4f6f9;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 200px;
  height: 250px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card h4 {
  margin-top: 15px;
  font-size: 1.2rem;
  color: #049bdc;
}

.card p {
  margin-top: 10px;
  color: #555;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

.card:active {
  transform: translateY(2px);
}

.footer {
  text-align: center;
  padding: 10px;
  background-color: #333;
  color: white;
}

.footer p {
  margin: 5px 0;
}

.footer a {
  color: #ffb800;
  text-decoration: none;
}

.footer a:hover {
  text-decoration: underline;
}

.button.primary {
  background-color: #049bdc;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
}

.button.secondary {
  background-color: #ffb800;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
}

.button:hover {
  opacity: 0.8;
}

.about, .publications, .team {
  padding: 40px;
  background-color: #ffffff;
  margin: 20px 0;
}

.about h3, .publications h3, .team h3{
  font-size: 2rem;
  margin-bottom: 20px;
}

.about-content, .card-container, .team-members {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.text, .image {
  flex: 1;
}

.text p {
  line-height: 1.6;
}

.card {
  background-color: #f4f6f9;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 15%;
}

.card h4 {
  margin-top: 15px;
  font-size: 1.2rem;
}

.card p {
  margin-top: 10px;
  color: #555;
}

.team-member {
  text-align: center;
}

.team-member img {
  width: 100%;
  height: 200px;
  border-radius: 50%;
}

.team-member h4 {
  font-size: 1.2rem;
  margin-top: 10px;
}

.team-member p {
  font-style: italic;
}

.footer {
  text-align: center;
  padding: 10px;
  background-color: #333;
  color: white;
}

.footer p {
  margin: 5px 0;
}

.footer a {
  color: #ffb800;
  text-decoration: none;
}

.footer a:hover {
  text-decoration: underline;
}

.button.primary {
  background-color: #049bdc;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
}

.button.secondary {
  background-color: #ffb800;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
}

.button:hover {
  opacity: 0.8;
}

</style> 