<template>
  <div class="home-container">
    <div class="intro-banner">
    </div>
    <section class="features">
      <h2 class="section-title">Welcome to Ginfinity API</h2>
      <div class="feature-cards">
        <p class="intro-p">Ginfinity API is a powerful tool for RNA sequence analysis, embedding calculation, and more. Lorem ipsum dolor sit amet consectetur adipisicing elit. Laboriosam ipsum eius, sapiente, distinctio numquam dolorem pariatur sunt, assumenda eligendi perspiciatis ratione officia id quam ipsa iste voluptas! Eligendi, impedit modi?
        </p>
      </div>
    </section>
    <section class="features">
      <h2 class="section-title">Our Features</h2>
      <div class="feature-cards">
        <div class="card">
          <h3 class="card-title">Compare RNA Sequences</h3>
          <p class="card-text">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nec tincidunt arcu, sit amet venenatis arcu.
            Aenean dictum est in dui blandit, nec elementum tortor lobortis.
          </p>
          <router-link to="/comparar-arn" class="btn-learn-more">Learn More</router-link>
        </div>
        <div class="card">
          <h3 class="card-title">Calculate Embeddings</h3>
          <p class="card-text">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nec tincidunt arcu, sit amet venenatis arcu.
            Aenean dictum est in dui blandit, nec elementum tortor lobortis.
          </p>
          <router-link to="/calcular-embeddings" class="btn-learn-more">Learn More</router-link>
        </div>
        <div class="card">
          <h3 class="card-title">Lorem ipsum dolor</h3>
          <p class="card-text">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nec tincidunt arcu, sit amet venenatis arcu.
            Aenean dictum est in dui blandit, nec elementum tortor lobortis.
          </p>  
          <router-link to="/" class="btn-learn-more">Learn More</router-link>
        </div>
      </div>
    </section>

    <section class="stats">
      <h2 class="section-title">Ginfinity Database Stats</h2>
      <div class="stats-grid">
        <div class="stat">
          <h3>8,246,911</h3>
          <p>Species</p>
        </div>
        <div class="stat">
          <h3>13</h3>
          <p>Phylogenetic Trees</p>
        </div>
        <div class="stat">
          <h3>4,094</h3>
          <p>Databases</p>
        </div>
      </div>
    </section>

    <section class="research">
      <h2 class="section-title">Learn More About Ginfinity API</h2>
      <p class="research-text">
        <router-link to="/" class="btn-learn-more">
          Discover Our Research and Publications
        </router-link>
      </p>
    </section>
  </div>
</template>

