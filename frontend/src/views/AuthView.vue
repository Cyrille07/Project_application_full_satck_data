<template>
  <div class="auth-page">
    <h1>🔐 Authentification</h1>
    <p class="subtitle">Génère ton token d'accès JWT avec ton identifiant employé</p>

    <div class="card">
      <h3>👨‍🍳 Connexion employé</h3>
      <form @submit.prevent="getToken">
        <input v-model="login.name" placeholder="Nom de l'employé" required />
        <input v-model="login.password" placeholder="Mot de passe" type="password" required />
        <input v-model="login.role" placeholder="Rôle (ex: Cashier, Cook...)" required />
        <button type="submit">Générer le token</button>
      </form>

      <!-- Affichage du résultat -->
      <pre v-if="response_auth.message">{{ response_auth.message }}</pre>
    </div>
  </div>
</template>




<script setup>

import { ref } from "vue";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";




//------------------Fonction : Générer un token---------------------------

const login = ref({name: "",password: "",role: ""});
const response_auth = ref({ message: "" });

const getToken = async () => {
  response_auth.value.message = "⏳ Envoi de la requête...";

  try {
    const res = await axios.post(`${API_URL}/auth/token`, login.value, {
      headers: { "Content-Type": "application/json" },
    });

    response_auth.value.message = `✅ Token généré :\n${res.data.access_token}`;
    localStorage.setItem("access_token", res.data.access_token);
  } catch (err) {
    const status = err.response?.status || "???";
    const detail = err.response?.data?.detail || err.message;
    response_auth.value.message = `❌ Erreur API (${status}) : ${detail}`;
  }
};

</script>





<style scoped>
.auth-page {
  text-align: center;
  padding: 2rem;
  font-family: "Segoe UI", sans-serif;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  width: 350px;
  margin: 0 auto;
}

input {
  display: block;
  width: 90%;
  margin: 0.5rem auto;
  padding: 0.6rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 14px;
}

button {
  background-color: #1d3557;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 0.5rem;
  font-weight: 600;
}

button:hover {
  background-color: #0b223f;
}

/* ✅ Zone d’affichage du token */
pre {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 1rem;
  text-align: left;
  white-space: pre-wrap;   /* ⚙️ Permet les retours à la ligne automatiques */
  word-wrap: break-word;   /* ⚙️ Coupe les lignes longues */
  max-width: 90%;          /* ⚙️ Limite la largeur du bloc */
  margin: 1rem auto 0;
  font-family: monospace;
  overflow-wrap: anywhere; /* ⚙️ Force la coupure si besoin */
}
</style>