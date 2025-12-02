import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TasksView from '../views/TasksView.vue'
import EmployeesView from '../views/EmployeesView.vue'
import AuthView from '../views/AuthView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/tasks', name: 'tasks', component: TasksView },
  { path: '/employees', name: 'employees', component: EmployeesView },
  { path: '/authentification', name: 'authentification', component: AuthView},
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
