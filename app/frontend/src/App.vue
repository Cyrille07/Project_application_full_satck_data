<template>
  <div id="app">
    <header class="navbar">
      <nav>
        <router-link to="/">
          <span>Accueil</span>
        </router-link>
        <router-link to="/tasks">
          <span>Voir les Tâches</span>
        </router-link>
        <router-link to="/employees">
          <span>Voir les Employés</span>
        </router-link>
        <router-link to="/authentification">
          <span>Authentification</span>
        </router-link>
      </nav>
    </header>

    <main class="main-content">
        <router-view />
    </main>
    
  </div>
</template>




<script setup>
// Le script setup peut rester vide ici
</script>






<style>
/* --- 1. Importation de la Police Manrope --- */
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;700&display=swap');

/* --- 2. Réinitialisation et Application Globale --- */
body {
  margin: 0;
  background-color: #f4f7f6; /* Fond léger */
  color: #333;
  font-family: 'Manrope', sans-serif; /* Application de la nouvelle police */
}

/* --- 3. Style de la Barre de Navigation (Header) --- */
.navbar {
  background-color: #3094ffff; /* Bleu primaire */
  padding: 15px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky; 
  top: 0;
  z-index: 100;
}

.navbar nav {
  display: flex;
  justify-content: center; /* Centrer les liens */
  gap: 30px; /* Espace entre les liens */
}

.navbar a {
  color: white;
  text-decoration: none;
  font-weight: 700; /* Bolder pour les liens */
  padding: 5px 10px;
  transition: background-color 0.3s, border-radius 0.3s;
}

.navbar a:hover {
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 5px;
}

/* Espacement spécifique des mots dans la nav */
.navbar a span {
  letter-spacing: 1px;
}

/* Style de la zone de contenu pour un bon espacement sous la barre */
.main-content {
    padding-top: 20px; 
}
</style>