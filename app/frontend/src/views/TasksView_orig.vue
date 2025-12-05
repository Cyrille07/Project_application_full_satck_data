<template>

  <div class="tasks-page">

    <h1>📌 Gestion des tâches</h1>
    <p class="subtitle">Créer, lister, modifier et supprimer des tâches</p>

    <div class="grid">

      <!-- 1️⃣ Créer une tâche -->
      <div class="card">
        <h3>📝 Créer une tâche</h3>
        <form @submit.prevent="createTask">
          <input v-model="newTask.author_id" placeholder="ID auteur" required />
          <input v-model="newTask.assigned_to_id" placeholder="ID employé assigné" />
          <input v-model="newTask.title" placeholder="Titre" required />
          <input v-model="newTask.description" placeholder="Description" required />
          <button type="submit">Créer</button>
        </form>
        <pre v-if="resp_create">{{ resp_create }}</pre>
      </div>

      <!-- 2️⃣ Lister toutes les tâches -->
      <div class="card">
        <h3>📋 Toutes les tâches</h3>
        <button @click="getAllTasks">🔄 Recharger</button>
        
        <ul>
          <li v-for="t in tasks" :key="t.id">
            <strong>{{ t.title }}</strong> — Auteur : {{ t.author_id }}
          </li>
        </ul>

        <pre v-if="resp_list">{{ resp_list }}</pre>
      </div>

      <!-- 3️⃣ Supprimer une tâche -->
      <div class="card">
        <h3>🗑️ Supprimer une tâche (auteur uniquement)</h3>
        <input v-model="deleteTaskId" placeholder="ID de la tâche" />
        <button class="danger" @click="deleteTask">Supprimer</button>
        <pre v-if="resp_delete_one">{{ resp_delete_one }}</pre>
      </div>

      <!-- 4️⃣ Supprimer toutes les tâches -->
      <div class="card">
        <h3>⚠️ Supprimer toutes les tâches</h3>
        <button class="danger" @click="deleteAllTasks">Tout supprimer</button>
        <pre v-if="resp_delete_all">{{ resp_delete_all }}</pre>
      </div>

      <!-- 5️⃣ Mettre à jour une tâche -->
      <div class="card">
        <h3>✏️ Modifier une tâche (auteur uniquement)</h3>
        
        <input v-model="updateTaskId" placeholder="ID de la tâche" required />
        
        <form @submit.prevent="updateTask">
          <input v-model="updateData.author_id" placeholder="Auteur" required />
          <input v-model="updateData.assigned_to_id" placeholder="Assigné à" />
          <input v-model="updateData.title" placeholder="Titre" required />
          <input v-model="updateData.description" placeholder="Description" required />
          <button class="update">Mettre à jour</button>
        </form>

        <pre v-if="resp_update">{{ resp_update }}</pre>
      </div>

    </div>
  </div>

</template>



import { ref } from "vue";
import axios from "axios";

const API_URL = "http://localhost:5001/tasks";

// --------- CREATE TASK ---------
const newTask = ref({
  author_id: "",
  assigned_to_id: "",
  title: "",
  description: "",
});

const resp_create = ref("");

const createTask = async () => {
  try {
    const res = await axios.post(`${API_URL}/`, newTask.value);
    resp_create.value = `✅ Tâche créée : ${res.data.title}`;
  } catch (err) {
    resp_create.value = `❌ Erreur : ${err.response?.data?.detail || err.message}`;
  }
};

// --------- GET ALL TASKS ---------
const tasks = ref([]);
const resp_list = ref("");

const getAllTasks = async () => {
  try {
    const res = await axios.get(`${API_URL}/`);
    tasks.value = res.data;
    resp_list.value = `📌 ${tasks.value.length} tâche(s) chargée(s)`;
  } catch (err) {
    resp_list.value = `❌ Erreur : ${err.response?.data?.detail || err.message}`;
  }
};

// --------- DELETE ONE TASK ---------
const deleteTaskId = ref("");
const resp_delete_one = ref("");

const deleteTask = async () => {
  const token = localStorage.getItem("access_token");

  try {
    const res = await axios.delete(`${API_URL}/${deleteTaskId.value}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    resp_delete_one.value = `🗑️ Tâche supprimée`;
  } catch (err) {
    resp_delete_one.value = `❌ Erreur : ${err.response?.data?.detail || err.message}`;
  }
};

// --------- DELETE ALL TASKS ---------
const resp_delete_all = ref("");

const deleteAllTasks = async () => {
  try {
    const res = await axios.delete(`${API_URL}/`);
    resp_delete_all.value = `🔥 ${res.data.message}`;
  } catch (err) {
    resp_delete_all.value = `❌ Erreur : ${err.response?.data?.detail || err.message}`;
  }
};

// --------- UPDATE TASK ---------
const updateTaskId = ref("");
const updateData = ref({
  author_id: "",
  assigned_to_id: "",
  title: "",
  description: "",
});

const resp_update = ref("");

const updateTask = async () => {
  const token = localStorage.getItem("access_token");

  try {
    const res = await axios.put(
      `${API_URL}/update_task_by_author_id`,
      updateData.value,
      {
        params: { task_id: updateTaskId.value },
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    resp_update.value = `✏️ Tâche modifiée : ${res.data.title}`;
  } catch (err) {
    resp_update.value = `❌ Erreur : ${err.response?.data?.detail || err.message}`;
  }
};




<style scoped>
.tasks-page {
  text-align: center;
  padding: 2rem;
  font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  background: #f4f5f7;
  min-height: 100vh;
}

h1 {
  margin-bottom: 0.25rem;
}

.subtitle {
  color: #666;
  margin-bottom: 2rem;
  font-size: 0.95rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  align-items: flex-start;
}

/* Cartes générales */
.card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
  text-align: left;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.card h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
}

/* Inputs & formulaires */
form {
  margin-top: 0.5rem;
}

input {
  display: block;
  width: 100%;
  margin: 0.4rem 0;
  padding: 0.55rem 0.7rem;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 0.9rem;
  box-sizing: border-box;
}

input:focus {
  border-color: #2b8a3e;
  outline: none;
  box-shadow: 0 0 0 2px rgba(43, 138, 62, 0.15);
}

/* Boutons */
button {
  display: inline-block;
  background-color: #2b8a3e;
  color: white;
  border: none;
  padding: 0.55rem 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
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

/* Liste des tâches */
ul {
  list-style: none;
  padding-left: 0;
  margin-top: 0.8rem;
  max-height: 230px;
  overflow-y: auto;
}

li {
  font-size: 0.9rem;
  padding: 0.35rem 0;
  border-bottom: 1px solid #eee;
}

li:last-child {
  border-bottom: none;
}

/* Zone de réponse */
pre {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 0.75rem;
  text-align: left;
  white-space: pre-wrap;
  word-wrap: break-word;
  max-width: 100%;
  margin-top: 0.75rem;
  font-family: "SFMono-Regular", Menlo, Monaco, Consolas, "Liberation Mono",
    "Courier New", monospace;
  font-size: 0.8rem;
}

/* Petits ajustements responsive */
@media (max-width: 600px) {
  .tasks-page {
    padding: 1.25rem;
  }

  .card {
    padding: 1.1rem;
  }
}
</style>
