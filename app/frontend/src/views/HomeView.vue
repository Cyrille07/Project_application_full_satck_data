<template>
  <div class="home">

    <main class="content-body">
      <h1>
          Bienvenue sur le Front End de notre application full stack Data
      </h1>

      <div :class="['api-status', { connected: !loading && message.includes('connecté') }]">
        <p v-if="loading">
          <span class="status-icon">⏳</span> Chargement du backend...
        </p>
        <p v-else-if="!loading && message.includes('Impossible')">
          <span class="status-icon">❌</span> Connexion API : {{ message }}
        </p>
        <p v-else>
          <span class="status-icon">✅</span> Connexion API : {{ message }}
        </p>
      </div>
      
      ---

      <div class="team-info">
        <h2> Membres de l'Équipe</h2>
        <p><strong>Étudiant :</strong> John Doe</p>
        <p><strong>Professeur :</strong> John Doe</p>
      </div>

      ---

      <div class="image-gallery">

        <div class="image-container">
          <div class="image-item">
            <img src="../image/pepite.png" alt="Aperçu des tâches" />
            
          </div>
          <div class="image-item">
            <img src="../image/logo_Esiee.jpg" alt="Aperçu des employés" />
            
          </div>
        </div>
      </div>

      ---


      <div class="project-description">
        <h3>💡 À propos du Projet</h3>
        <p>
          Ce projet full stack est une plateforme moderne de gestion de données. 
          Il permet d'interagir avec notre API backend pour la manipulation des tâches et des informations sur les employés. 
          L'objectif est de fournir une interface utilisateur intuitive et réactive, construite avec Vue.js, pour visualiser 
          l'état de l'application et des données critiques.
        </p>
      </div>

      ---



    </main>
  </div>
</template>


<script setup>

import { ref, onMounted } from "vue"
import axios from "axios"

const message = ref("")
const loading = ref(true)
// L'URL de l'API est visible ici comme demandé
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001"

const checkHealth = async () => {
  try {
    const res = await axios.get(`${API_URL}/health/`)
    // Assurez-vous que le message renvoyé par l'API contient un mot clé comme "connecté" ou "en ligne"
    message.value = res.data.message
  } catch (err) {
    message.value = "❌ Impossible de contacter l'API"
  } finally {
    loading.value = false
  }
}

onMounted(checkHealth)
</script>



<style>
.home {
  text-align: center;
}

.content-body {
  /* On retire le margin-top car App.vue gère déjà l'espacement */
  padding: 0 20px;
}

.content-body h1 {
  color: #007bffff;
  font-size: 3.5em;
  margin-bottom: 30px;
}

/* --- Style de l'État de l'API --- */
.api-status {
  margin: 20px auto;
  padding: 15px;
  border-radius: 8px;
  max-width: 450px;
  border: 1px solid #ccc;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.api-status p {
  margin: 0;
  font-size: 1.1em;
  color: #dc3545; /* Rouge pour l'erreur par défaut/chargement */
}

.api-status.connected p {
  color: #28a745; /* Vert pour la connexion réussie */
}

.status-icon {
  margin-right: 5px;
}

/* --- Style de la Section Équipe --- */
.team-info {
  margin-top: 40px;
  padding: 20px;
  border-top: 2px solid #ccc;
  border-bottom: 2px solid #ccc; /* Ajout d'une ligne en bas pour encadrer */
  display: inline-block;
  max-width: 450px;
  width: 100%;
}

.team-info h2 {
  color: #333;
  margin-bottom: 15px;
  font-size: 1.5em;
}

.team-info p {
  text-align: left;
  line-height: 1.6;
}

/* --- NOUVEAU : Style de la Description du Projet --- */
.project-description {
  margin: 40px auto;
  padding: 20px 30px;
  max-width: 700px;
  background-color: #e9f7ff; /* Fond bleu très clair */
  border-left: 5px solid #007bff;
  border-radius: 4px;
  text-align: left;
}

.project-description h3 {
  color: #007bff;
  margin-top: 0;
  font-size: 1.3em;
}

.project-description p {
  line-height: 1.6;
  color: #555;
}

/* --- Style de la Galerie d'Images CÔTE À CÔTE --- */
.image-gallery {
  margin: 50px auto;
  max-width: 600px; /* <--- DIMINUEZ LA LARGEUR MAXIMALE DE LA GALERIE GLOBALE */
}

.image-gallery h2 {
    color: #333;
    margin-bottom: 25px;
}

.image-container {
  display: flex; 
  justify-content: center; 
  gap: 20px; /* <--- DIMINUEZ L'ESPACE ENTRE LES IMAGES SI NÉCESSAIRE */
  flex-wrap: wrap; 
}

.image-item {
  width: 35%; /* <--- DIMINUEZ LA LARGEUR DE CHAQUE CONTENEUR D'IMAGE */
  min-width: 200px; /* <--- DÉFINISSEZ UNE LARGEUR MINIMALE POUR NE PAS QU'ELLES SOIENT TROP PETITES */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden; 
}

.image-item img {
  width: 100%; /* L'image prend 100% de la largeur de son conteneur */
  height: auto;
  display: block; 
  border-bottom: 1px solid #eee;
}

.image-item .caption {
  padding: 10px 0;
  margin: 0;
  background-color: white;
  font-weight: 700;
  font-size: 0.9em;
  color: #007bff;
}
</style>