<template>
  <div class="Task-page">
    <h1>📋 Gestion des Tâches</h1>
    <p class="subtitle">Interagissez directement avec l’API FastAPI</p>

    <div class="grid">

      <!-- 1️⃣ Créer une Task -->
      <div class="card">
        <h3>➕ Ajouter une tâche</h3>
        <form @submit.prevent="createTask">
          <input v-model="newTask.title" placeholder="Titre" required />
          <input v-model="newTask.content" placeholder="Contenu" required />
          <input v-model="newTask.author_id" placeholder="ID auteur" required />
          <input v-model="newTask.recipient_id" placeholder="ID destinataire (recipient_id)" />
          <button type="submit">Créer</button>
        </form>

        <!-- Message de réponse -->
        <pre v-if="responses_create_task.create">{{ responses_create_task.create }}</pre>
      </div>


      <!-- 2️⃣ Lister toutes les tâches -->
      <div class="card">
        <h3>📋 Liste des tâches</h3>
        <button @click="getAllTasks" class="refresh-btn">🔄 Recharger</button>

        <div v-if="responses_get_tasks.error" class="error-box">
          ❌ {{ responses_get_tasks.error }}
        </div>

        <ul v-if="tasksList.length > 0" class="task-list">
          <li v-for="task in tasksList" :key="task.id" class="task-item">

            <strong>📝 {{ task.title }}</strong>
            <br />

            📄 <em>{{ task.content }}</em>
            <br /><br />

            🆔 <strong>ID tâche :</strong> {{ task.id }}  
            <br />
            🕒 Créée le : {{ formatDate(task.created_at) }}
            <br /><br />

            ✍️ <strong>Auteur :</strong>  
            <br />
            • Nom : {{ task.author.name }}  
            <br />
            • Rôle : {{ task.author.role }}  
            <br />
            • ID : {{ task.author_id }}
            <br /><br />

            🎯 <strong>Assignée à :</strong>  
            <br />
            • Nom : {{ task.recipient.name }}  
            <br />
            • Rôle : {{ task.recipient.role }}  
            <br />
            • ID : {{ task.recipient_id }}

          </li>
        </ul>

        <p v-else class="empty-list">Aucune tâche trouvée.</p>
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



      <!-- 4️⃣ Rechercher tâches par auteur -->
      <div class="card">
        <h3>🧑‍💻 Tâches écrites par un employé</h3>

        <form @submit.prevent="getTasksByAuthor">
          <input v-model="searchAuthorId" placeholder="ID de l'auteur" required />
          <button type="submit">Rechercher</button>
        </form>

        <!-- Message d'état -->
        <p v-if="response_get_by_author.message">{{ response_get_by_author.message }}</p>

        <!-- Liste des tâches -->
        <ul v-if="tasks_by_author.length > 0">
          <li v-for="task in tasks_by_author" :key="task.id">
            <strong>{{ task.title }}</strong> — {{ task.content }}
            <br />
            ✍️ Auteur : <strong>{{ task.author.name }}</strong> ({{ task.author.role }})
            <br />
            🎯 Assignée à : {{ task.recipient.name }} ({{ task.recipient.role }})
            <br />
            📅 {{ formatDate(task.created_at) }}
            <br /><br />
          </li>
        </ul>
      </div>


      <!-- 5️⃣ Rechercher tâches par destinataire (recipient) -->
      <div class="card">
        <h3>🎯 Tâches reçues par un employé</h3>

        <form @submit.prevent="getTasksByRecipient">
          <input v-model="searchRecipientId" placeholder="ID du destinataire" required />
          <button type="submit">Rechercher</button>
        </form>

        <!-- Message d'état -->
        <p v-if="response_get_by_recipient.message">{{ response_get_by_recipient.message }}</p>

        <!-- Liste des tâches -->
        <ul v-if="tasks_by_recipient.length > 0">
          <li v-for="task in tasks_by_recipient" :key="task.id">
            <strong>{{ task.title }}</strong> — {{ task.content }}
            <br />
            🧑🎯 Destinataire : <strong>{{ task.recipient.name }}</strong> ({{ task.recipient.role }})
            <br />
            ✍️ Auteur : {{ task.author.name }} ({{ task.author.role }})
            <br />
            📅 {{ formatDate(task.created_at) }}
            <br /><br />
          </li>
        </ul>
      </div>


      <!-- 6️⃣ Supprimer une tâche -->
      <div class="card">
        <h3>🗑️ Supprimer une tâche</h3>

        <form @submit.prevent="deleteTaskById">
          <input v-model="deleteTaskId" placeholder="ID de la tâche" required />
          <button type="submit" class="danger">Supprimer</button>
        </form>

        <pre v-if="response_delete_task.message">{{ response_delete_task.message }}</pre>
      </div>


      <!-- 7️⃣ Supprimer toutes les tâches (Chief only) -->
      <div class="card danger-card">
        <h3>🗑️ Supprimer toutes les tâches</h3>

        <p class="warning">⚠️ Action réservée au Chief_of_resto</p>

        <form @submit.prevent="deleteAllTasks">
          <input
            v-model="chiefIdForTaskDelete"
            placeholder="ID du Chief connecté"
            required
          />
          <button class="danger" type="submit">Supprimer toutes les tâches</button>
        </form>

        <pre v-if="response_delete_all_tasks.message">
          {{ response_delete_all_tasks.message }}
        </pre>
      </div>







    </div>
  </div>
</template>





<script setup>
import { ref } from "vue";
import axios from "axios";


// Base API pour les tasks
const TASKS_API_URL = "http://localhost:5001/tasks";

// Formatage date
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString("fr-FR");
};





//--------------------------- Fonction Create Task---------------------------
const newTask = ref({
  title: "",
  content: "",
  author_id: "",
  recipient_id: "",
});
const responses_create_task = ref({ create: "" });

const createTask = async () => {
  responses_create_task.value.create = "⏳ Création de la tâche en cours...";

  try {
    const res = await axios.post(`${TASKS_API_URL}/`, newTask.value, {
      headers: { "Content-Type": "application/json" },
    });

    responses_create_task.value.create =
      `✅ Tâche créée avec succès : "${res.data.title}" (id: ${res.data.id})`;

    newTask.value = {
      title: "",
      content: "",
      author_id: "",
      recipient_id: "",
    };

  } catch (err) {
    responses_create_task.value.create =
      `❌ Erreur API : ${err.response?.data?.detail || err.message}`;
  }
};


// ---------------------- GET ALL TASKS ------------------------------
const tasksList = ref([]);
const responses_get_tasks = ref({ error: "" });

const getAllTasks = async () => {
  responses_get_tasks.value.error = "";
  tasksList.value = [];

  try {
    const res = await axios.get(`${TASKS_API_URL}/`, {
      headers: { "Content-Type": "application/json" },
    });

    tasksList.value = res.data;
  } catch (err) {
    console.error("Erreur API (getAllTasks) :", err);

    if (err.response) {
      responses_get_tasks.value.error =
        `Erreur API (${err.response.status}) : ${
          err.response.data.detail || "Erreur inconnue."
        }`;
    } else if (err.request) {
      responses_get_tasks.value.error =
        "Erreur réseau : impossible de contacter le serveur.";
    } else {
      responses_get_tasks.value.error = `Erreur inattendue : ${err.message}`;
    }
  }
};



// ---------------------- GET ALL EMPLOYEES ----------------------
const employees = ref([]);
const responses_getEmployees = ref({ list: "" });

const getEmployees = async () => {
  try {
    const res = await axios.get("http://localhost:5001/employees/", {
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


// ---------------------- GET TASK BY AUTHOR ID ----------------------
const searchAuthorId = ref("");
const tasks_by_author = ref([]);
const response_get_by_author = ref({ message: "" });

const getTasksByAuthor = async () => {
  tasks_by_author.value = [];
  response_get_by_author.value.message = "⏳ Chargement des tâches...";

  try {
    const res = await axios.get(`${TASKS_API_URL}/taskauthor/${searchAuthorId.value}`);

    if (res.data.length === 0) {
      response_get_by_author.value.message = "⚠️ Aucun résultat trouvé.";
      return;
    }

    tasks_by_author.value = res.data;
    response_get_by_author.value.message = `✅ ${res.data.length} tâche(s) trouvée(s).`;

  } catch (err) {
    console.error("Erreur API (author):", err);

    if (err.response) {
      const detail =
        typeof err.response.data.detail === "string"
          ? err.response.data.detail
          : JSON.stringify(err.response.data);

      response_get_by_author.value.message =
        `❌ Erreur API (${err.response.status}) : ${detail}`;
    } else {
      response_get_by_author.value.message = "❌ Erreur réseau ou inattendue.";
    }
  }
};


// ---------------------- GET TASK BY RECIPIENT ID ----------------------
const searchRecipientId = ref("");
const tasks_by_recipient = ref([]);
const response_get_by_recipient = ref({ message: "" });

const getTasksByRecipient = async () => {
  tasks_by_recipient.value = [];
  response_get_by_recipient.value.message = "⏳ Chargement des tâches...";

  try {
    const res = await axios.get(`${TASKS_API_URL}/taskrecipient/${searchRecipientId.value}`);

    if (res.data.length === 0) {
      response_get_by_recipient.value.message = "⚠️ Aucun résultat trouvé.";
      return;
    }

    tasks_by_recipient.value = res.data;
    response_get_by_recipient.value.message =
      `✅ ${res.data.length} tâche(s) trouvée(s) pour ce destinataire.`;

  } catch (err) {
    console.error("Erreur API (recipient):", err);

    if (err.response) {
      const detail =
        typeof err.response.data.detail === "string"
          ? err.response.data.detail
          : JSON.stringify(err.response.data);

      response_get_by_recipient.value.message =
        `❌ Erreur API (${err.response.status}) : ${detail}`;
    } else {
      response_get_by_recipient.value.message = "❌ Erreur réseau ou inattendue.";
    }
  }
};




// ---------------------- DELETE TASK BY ID ----------------------
const deleteTaskId = ref("");
const response_delete_task = ref({ message: "" });

const deleteTaskById = async () => {
  response_delete_task.value.message = "⏳ Suppression en cours...";

  try {
    const res = await axios.delete(`${TASKS_API_URL}/deltask/${deleteTaskId.value}`, {
      headers: { "Content-Type": "application/json" },
    });

    response_delete_task.value.message = 
      `✅ Tâche supprimée : ${res.data.title} (${res.data.id})`;

    deleteTaskId.value = "";

  } catch (err) {
    console.error("Erreur API (delete):", err);

    if (err.response) {
      const detail =
        typeof err.response.data.detail === "string"
          ? err.response.data.detail
          : JSON.stringify(err.response.data);

      response_delete_task.value.message =
        `❌ Erreur API (${err.response.status}) : ${detail}`;

    } else if (err.request) {
      response_delete_task.value.message = 
        "❌ Erreur réseau — impossible de contacter le serveur.";
    } else {
      response_delete_task.value.message = 
        `❌ Erreur inattendue : ${err.message}`;
    }
  }
};



// ---------------------- DELETE ALL TASKS ----------------------
const chiefIdForTaskDelete = ref("");
const response_delete_all_tasks = ref({ message: "" });

const deleteAllTasks = async () => {
  response_delete_all_tasks.value.message = "⏳ Vérification du token...";

  // Token stocké en local (unique source d'identité)
  const localToken = localStorage.getItem("access_token");

  if (!localToken) {
    response_delete_all_tasks.value.message =
      "❌ Aucun token trouvé. Veuillez vous authentifier d'abord.";
    return;
  }

  // Vérifier que l'utilisateur a entré l'ID correspondant au token
  if (!chiefIdForTaskDelete.value.trim()) {
    response_delete_all_tasks.value.message =
      "❌ Veuillez saisir votre ID avant de supprimer toutes les tâches.";
    return;
  }

  response_delete_all_tasks.value.message =
    "⏳ Suppression de toutes les tâches...";

  try {
    const res = await axios.delete(
      `${TASKS_API_URL}/deletealltask/${chiefIdForTaskDelete.value}`,
      {
        headers: {
          Authorization: `Bearer ${localToken}`,
          "Content-Type": "application/json",
        },
      }
    );

    // Succès
    response_delete_all_tasks.value.message = `✅ Toutes les tâches ont été supprimées.\nTâches retournées:\n${JSON.stringify(
      res.data,
      null,
      2
    )}`;
  } catch (err) {
    console.error("Erreur API (delete all tasks):", err);

    if (err.response) {
      const detail =
        typeof err.response.data.detail === "string"
          ? err.response.data.detail
          : JSON.stringify(err.response.data);

      response_delete_all_tasks.value.message = `❌ Erreur API (${err.response.status}) : ${detail}`;
    } else if (err.request) {
      response_delete_all_tasks.value.message =
        "❌ Erreur réseau — impossible de contacter le serveur.";
    } else {
      response_delete_all_tasks.value.message = `❌ Erreur inattendue : ${err.message}`;
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
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
}


.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
  gap: 1.5rem;
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 3 colonnes fixes */
  gap: 1.5rem;
  padding: 1rem;
}

.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  transition: 0.3s ease;
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 14px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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

.task-list {
  list-style: none;
  padding: 0;
}

.task-item {
  background: #f7f7f7;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  border-left: 5px solid #4e73df;
  line-height: 1.5;
}

.refresh-btn {
  margin-bottom: 15px;
  padding: 8px 14px;
  background: #4e73df;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.refresh-btn:hover {
  background: #3b5bb8;
}

.empty-list {
  text-align: center;
  color: #888;
  margin-top: 10px;
}

.error-box {
  color: #b30000;
  background: #ffe5e5;
  border-left: 4px solid #b30000;
  padding: 10px;
  border-radius: 6px;
  margin: 10px 0;
}

.Task-page h1 {
  text-align: center;
  margin-bottom: 1rem;
}


/* Mobile & tablettes : 1 carte par ligne */
@media (max-width: 900px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .grid {
    grid-template-columns: repeat(1, 1fr);
  }
}



</style>
