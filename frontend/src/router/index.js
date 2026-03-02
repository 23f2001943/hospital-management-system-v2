import { createRouter, createWebHistory } from "vue-router";

import Login from "../pages/Login.vue";
import AdminDashboard from "../pages/admin/AdminDashboard.vue";
import DoctorDashboard from "../pages/doctor/DoctorDashboard.vue";
import PatientDashboard from "../pages/patient/PatientDashboard.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/admin", component: AdminDashboard },
  { path: "/doctor", component: DoctorDashboard },
  { path: "/patient", component: PatientDashboard }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;