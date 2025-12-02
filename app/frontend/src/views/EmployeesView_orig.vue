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
          <input v-model="newEmployee.role" placeholder="Rôle (ex: Cashier, Manager...)" required />
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
        <pre v-if="responses_.create">{{ responses_create_emloyee.create }}</pre>
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
      </div>


      <!-- 4️⃣ Supprimer un employé -->
      <div class="card">
        <h2>🗑️ Supprimer un employé</h2>
        <input v-model="deleteId" placeholder="ID employé" />
        <button class="danger" @click="deleteEmployee">Supprimer</button>
        <p v-if="responses.delete">{{ responses.delete }}</p>
      </div>

      <!-- 5️⃣ Supprimer tous les employés -->
      <div class="card danger-card">
        <h3>⚠️ Supprimer tous les employés</h3>
        <p class="warning">Action réservée au Chef du restaurant</p>

        <input
          v-model="chiefId"
          placeholder="ID du Chef (employee_id)"
          required
        />
        <button class="danger" @click="deleteAllEmployees">Supprimer tout le personnel</button>

        <pre v-if="responses_delete_all.delete_all">{{ responses_delete_all.delete_all }}</pre>
      </div>



    </div>
  </div>
</template>




<script setup>
import { ref } from "vue";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001/employees";

const updateData = ref({ name: "", role: "" });


const deleteId = ref("");
const updateId = ref("");

const employeeFound = ref(null);
const employees = ref([]);
const responses = ref({ create: "", delete: "", update: "" });





// --------------------------- Fonctions API ---------------------------

//----------------Fonction : Créer un employé-------------

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
  } 
    catch (err) {
    console.error("Erreur API :", err);
    responses_create_emloyee.value.create = "❌ Erreur d’exécution\n";

    try {
      const test = await fetch(`${API_URL}/`, {
        method: "POST",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: "string",
          password: "string",
          role: "string",
        }),
      });

      const text = await test.text();

      if (test.ok) {
        responses_create_emloyee.value.create += `\n${text}`;} 
        else {responses_create_emloyee.value.create += `\nRéponse :\n${text}`;}
    } 
    catch (curlErr) { responses_create_emloyee.value.create += `❌ Curl échoué : impossible d’atteindre ${API_URL}/`;}
  }
};





//🔹Rechercher un employé par ID (exactement comme le curl)
const employeeData = ref(null)
const searchedResult = ref("")
const message = ref("")
const searchId = ref("")

const getEmployeeById = async () => {
  employeeData.value = null
  searchedResult.value = ""
  message.value = "⏳ Envoi de la requête..."

  try {
    const res = await axios.get(`http://localhost:5001/employees/${searchId.value}`, {
      headers: { "Content-Type": "application/json" },
      validateStatus: () => true
    })

    if (res.status >= 200 && res.status < 300) {
      // ✅ Affichage structuré
      employeeData.value = res.data
      message.value = "✅ Requête réussie"
    } else {
      // ❌ Affichage du JSON brut en cas d’erreur
      searchedResult.value = JSON.stringify(res.data, null, 2)
      message.value = "❌ Requête échouée"
    }

  } catch (err) {
    searchedResult.value = JSON.stringify({ error: err.message }, null, 2)
    message.value = "❌ Requête échouée"
  }
}




//🔹Récupérer tous les employés
const getEmployees = async () => {
  try {
    const res = await axios.get("http://localhost:5001/employees/")
    employees.value = res.data
    message.value = `✅ ${employees.value.length} employé(s) chargé(s)`
  } catch (err) {
    console.error(err)
    message.value = "❌ Erreur lors du chargement des employés"
  }
}


const deleteEmployee = async () => {
  try {
    await axios.delete(`${API_URL}/${deleteId.value}`);
    responses.value.delete = "✅ Employé supprimé avec succès";
  } catch (err) {
    responses.value.delete = "❌ Échec de la suppression";
  }
};

const updateEmployee = async () => {
  try {
    const res = await axios.put(`${API_URL}/updateme`, updateData.value, {
      params: { employee_id: updateId.value },
    });
    responses.value.update = `✅ Employé ${res.data.name} mis à jour`;
  } catch (err) {
    responses.value.update = "❌ Erreur de mise à jour";
  }
};

//------------------Fonction : DELETE All employees---------------------------
const chiefId = ref("");
const responses_delete_all = ref({ delete_all: "" });

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
