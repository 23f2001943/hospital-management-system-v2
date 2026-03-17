import { createRouter, createWebHistory } from "vue-router";

import Login from "../pages/Login.vue";
import AdminDashboard from "../pages/admin/AdminDashboard.vue";
import DoctorDashboard from "../pages/doctor/DoctorDashboard.vue";
import PatientDashboard from "../pages/patient/PatientDashboard.vue";
import DoctorManagement from "../pages/admin/DoctorManagement.vue";
import PatientManagement from "../pages/admin/PatientManagement.vue";
import AppointmentManagement from "../pages/admin/AppointmentManagement.vue"
import DoctorPatients from "../pages/doctor/DoctorPatients.vue"
import DoctorAppointments  from "../pages/doctor/DoctorAppointments.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", component: Login },
  { path: "/admin", component: AdminDashboard },
  { path: "/doctor", component: DoctorDashboard },
  { path: "/patient", component: PatientDashboard },
  {path: "/admin/doctors", component: DoctorManagement },
  { path: "/admin/patients", component: PatientManagement },
  { path: "/admin/appointments", component: AppointmentManagement },
  { path: "/doctor/patients", component: DoctorPatients },
  { path: "/doctor/appointments", component: DoctorAppointments }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;



