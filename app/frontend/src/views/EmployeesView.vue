<template>
  <div class="employees-page">
    <h1>👥 Gestion des employés</h1>
    <p class="subtitle">Interagissez directement avec l’API FastAPI</p>

    <div class="grid">

  
      <!-- 1️⃣ Créer un employé -->
      <div class="card">
        <h3>➕ Ajouter un employé</h3>
        <form @submit.prevent="createEmployee">
          <input v-model="newEmployee.name" placeholder="Nom" required />
          <input v-model="newEmployee.password" placeholder="Mot de passe" required type="password" />
          <input v-model="newEmployee.role" placeholder="Rôle (ex: Cashier, Cook...)" required />
          <button type="submit">Créer l'employé</button>
        </form>
        <!-- Message affiché -->
        <pre v-if="responses_create_emloyee.create">{{ responses_create_emloyee.create }}</pre>
      </div>



      <!-- 2️⃣ Rechercher un employé -->
      <div class="card">
        <h3>🔍 Rechercher un employé</h3>
        <form @submit.prevent="getEmployeeById">
          <input v-model="searchId" placeholder="Entrer l'ID de l'employé" required />
          <button type="submit">Rechercher</button>
        </form>
        <!-- Message affiché -->
        <pre v-if="responses_getEmployeeById.get">{{ responses_getEmployeeById.get }}</pre>
      </div>



      <!-- 3️⃣ Lister tous les employés -->
      <div class="card">
        <h3>📋 Liste des employés</h3>
        <button @click="getEmployees">🔄 Recharger</button>
          <ul>
            <li v-for="emp in employees" :key="emp.id">
              <strong>{{ emp.name }}</strong> — {{ emp.role }}  
              <span class="id">ID: {{ emp.id }}</span>
            </li>
          </ul>
          <!-- Message affiché -->
          <p v-if="responses_getEmployees.list">{{ responses_getEmployees.list }}</p>
      </div>



      <!-- 4️⃣ Supprimer un employé -->
      <div class="card">
        <h3>🗑️ Supprimer un employé</h3>
        <input v-model="deleteId" placeholder="ID employé" required />
        <button class="danger" @click="deleteEmployee">Supprimer</button>
        <p v-if="responses_del.delete">{{ responses_del.delete }}</p>
      </div>



      <!-- 5️⃣ Supprimer tous les employés -->
      <div class="card danger-card">
        <h3>⚠️ Supprimer tous les employés</h3>
        <p class="warning">Action réservée au Chef du restaurant</p>

        <input
          v-model="chiefId"
          placeholder="Entrer l'ID du Chef (employee_id)"
          required
        />
        <button class="danger" @click="deleteAllEmployees">Supprimer tout le personnel</button>

        <pre v-if="responses_delete_all.delete_all">{{ responses_delete_all.delete_all }}</pre>
      </div>



      <!-- 6️⃣ Mettre à jour les informations d’un employé -->
      <div class="card">
        <h3>✏️ Mettre à jour les informations d’un employé</h3>
        <p class="subtitle">Vérification par token obligatoire</p>

        <form @submit.prevent="updateEmployeeByToken">
          <input v-model="employeeUpdateToken" placeholder="Entrer le token JWT de l’employé" required />
          <input v-model="updateData.name" placeholder="Nouveau nom" required />
          <input v-model="updateData.password" placeholder="Nouveau mot de passe" required type="password" />
          <input v-model="updateData.role" placeholder="Nouveau rôle (ex: Cashier, Cook...)" required />
          <button type="submit">Mettre à jour</button>
        </form>

        <pre v-if="responses_update.update">{{ responses_update.update }}</pre>
      </div>



    </div>
  </div>





</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const API_URL = "http://localhost:5001/employees";



//------------------Fonction : Créer un employé---------------------------

// Données du formulaire
const newEmployee = ref({ name: "", password: "", role: "" });
// Message de retour
const responses_create_emloyee = ref({ create: "" });

const createEmployee = async () => {
  try {
    const res = await axios.post(`${API_URL}/`, newEmployee.value, {
      headers: { "Content-Type": "application/json" },
    });

    responses_create_emloyee.value.create = `✅ Employé "${res.data.name}" créé avec succès !`;
    newEmployee.value = { name: "", password: "", role: "" };
  } catch (err) {
    console.error("Erreur API :", err);

    if (err.response) {
      // Erreur renvoyée par FastAPI
      const detail =
        typeof err.response.data.detail === "string"
          ? err.response.data.detail
          : JSON.stringify(err.response.data);

      responses_create_emloyee.value.create = `❌ Erreur API (${err.response.status}) : ${detail}`;
    } else if (err.request) {
      responses_create_emloyee.value.create =
        "❌ Erreur réseau — impossible de contacter le serveur";
    } else {
      responses_create_emloyee.value.create = `❌ Erreur inattendue : ${err.message}`;
    }
  }
};



//------------------Fonction : Get Employee by Id---------------------------
const searchId = ref("");
const responses_getEmployeeById = ref({ get: "" });

const getEmployeeById = async () => {
  responses_getEmployeeById.value.get = "⏳ Envoi de la requête...";

  try {
    const res = await axios.get(`${API_URL}/${searchId.value}`, {
      headers: { "Content-Type": "application/json" },
      validateStatus: () => true, // on gère nous-même le statut
    });

    if (res.status >= 200 && res.status < 300) {
      // ✅ succès → on affiche le JSON formaté
      responses_getEmployeeById.value.get =
        "✅ Requête réussie\n\n" + JSON.stringify(res.data, null, 2);
    } else {
      // ❌ erreur côté API → on affiche la réponse brute
      responses_getEmployeeById.value.get =
        `❌ Requête échouée (status ${res.status})\n\n` +
        JSON.stringify(res.data, null, 2);
    }
  } catch (err) {
    // ❌ erreur réseau / autre
    responses_getEmployeeById.value.get =
      "❌ Erreur d’exécution\n\n" + (err.message || "Erreur inconnue");
  }
};



//------------------Fonction : Get ALL Employee---------------------------

const employees = ref([]);
const responses_getEmployees = ref({ list: "" });

const getEmployees = async () => {
  try {
    const res = await axios.get(`${API_URL}/`, {
      headers: { "Content-Type": "application/json" },
    });

    // ✅ Succès
    employees.value = res.data;
    responses_getEmployees.value.list = `✅ ${employees.value.length} employé(s) chargé(s)`;
  } catch (err) {
    console.error("Erreur API :", err);

    if (err.response) {
      // ❌ Erreur renvoyée par le backend FastAPI
      const detail =
        typeof err.response.data.detail === "string"
          ? err.response.data.detail
          : JSON.stringify(err.response.data);

      responses_getEmployees.value.list = `❌ Erreur API (${err.response.status}) : ${detail}`;
    } else if (err.request) {
      // 💀 Erreur réseau (pas de réponse du serveur)
      responses_getEmployees.value.list =
        "❌ Erreur réseau — impossible de contacter le serveur";
    } else {
      // ⚙️ Autre erreur JS
      responses_getEmployees.value.list = `❌ Erreur inattendue : ${err.message}`;
    }
  }
};



//------------------Fonction : DELETE Employee by ID---------------------------
const deleteId = ref(""); // ID saisi par l'utilisateur
const responses_del = ref({ delete: "" }); // message à afficher


const deleteEmployee = async () => {
  responses_del.value.delete = "⏳ Suppression en cours...";

  try {
    const res = await axios.delete(`${API_URL}/${deleteId.value}`, {
      headers: { "Content-Type": "application/json" },
    });

    responses_del.value.delete = `✅ Employé avec ID ${deleteId.value} supprimé avec succès`;
    deleteId.value = "";
  } catch (err) {
    console.error("Erreur API :", err);

    if (err.response) {
      const detail =
        typeof err.response.data.detail === "string"
          ? err.response.data.detail
          : JSON.stringify(err.response.data);

      responses_del.value.delete = `❌ Erreur API (${err.response.status}) : ${detail}`;
    } else if (err.request) {
      responses_del.value.delete =
        "❌ Erreur réseau — impossible de contacter le serveur";
    } else {
      responses_del.value.delete = `❌ Erreur inattendue : ${err.message}`;
    }
  }
};



//------------------Fonction : DELETE All employees---------------------------
const responses_delete_all = ref({ delete_all: "" });
const chiefId = ref("");

const deleteAllEmployees = async () => {
  responses_delete_all.value.delete_all = "⏳ Suppression en cours...";

  const token = localStorage.getItem("access_token");

  if (!token) {
    responses_delete_all.value.delete_all = "❌ Aucun token trouvé. Veuillez vous authentifier d’abord.";
    return;
  }

  try {
    const res = await axios.delete(`${API_URL}/delete_all/${chiefId.value}`, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    responses_delete_all.value.delete_all = `✅ ${res.data.message}`;
  } catch (err) {
    console.error("Erreur API :", err);

    if (err.response) {
      const detail =
        typeof err.response.data.detail === "string"
          ? err.response.data.detail
          : JSON.stringify(err.response.data);
      responses_delete_all.value.delete_all = `❌ Erreur API (${err.response.status}) : ${detail}`;
    } else if (err.request) {
      responses_delete_all.value.delete_all =
        "❌ Erreur réseau — impossible de contacter le serveur.";
    } else {
      responses_delete_all.value.delete_all = `❌ Erreur inattendue : ${err.message}`;
    }
  }
};





//------------------Fonction : Update employee by Id ---------------------------

const updateData = ref({ name: "", password: "", role: "" });
const employeeUpdateToken = ref(""); // Token entré manuellement
const responses_update = ref({ update: "" });

const updateEmployeeByToken = async () => {
  responses_update.value.update = "⏳ Vérification du token...";

  // Token stocké localement (celui du user connecté)
  const localToken = localStorage.getItem("access_token");

  // Vérifier la correspondance des tokens
  if (!localToken) {
    responses_update.value.update = "❌ Aucun token local trouvé. Veuillez vous authentifier d’abord.";
    return;
  }

  if (employeeUpdateToken.value.trim() !== localToken.trim()) {
    responses_update.value.update =
      "❌ Le token saisi ne correspond pas au token d’authentification actuel. Accès refusé.";
    return;
  }

  // Si tout est bon, on appelle le backend
  responses_update.value.update = "⏳ Envoi de la requête de mise à jour...";

  try {
    const res = await axios.put(`${API_URL}/employees/updateme`, updateData.value, {
      headers: {
        Authorization: `Bearer ${localToken}`,
        "Content-Type": "application/json",
      },
    });

    responses_update.value.update = `✅ Employé mis à jour avec succès : ${res.data.name} (${res.data.role})`;
  } catch (err) {
    console.error("Erreur API :", err);

    if (err.response) {
      const detail =
        typeof err.response.data.detail === "string"
          ? err.response.data.detail
          : JSON.stringify(err.response.data);
      responses_update.value.update = `❌ Erreur API (${err.response.status}) : ${detail}`;
    } else if (err.request) {
      responses_update.value.update = "❌ Erreur réseau — impossible de contacter le serveur.";
    } else {
      responses_update.value.update = `❌ Erreur inattendue : ${err.message}`;
    }
  }
};




</script>





<style scoped>
.employees-page {
  text-align: center;
  padding: 2rem;
  font-family: "Segoe UI", sans-serif;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
  gap: 1.5rem;
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  transition: 0.3s ease;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
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
  background-color: #2b8a3e;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 0.5rem;
  font-weight: 600;
}

button:hover {
  background-color: #1f6b31;
}

button.danger {
  background-color: #e63946;
}

button.danger:hover {
  background-color: #b02128;
}

button.update {
  background-color: #1d3557;
}

button.update:hover {
  background-color: #0b223f;
}

pre {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 1rem;
  text-align: left;
  white-space: pre-wrap;
  font-family: monospace;
}
</style>
