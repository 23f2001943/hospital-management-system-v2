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
import Register from "../pages/Register.vue";
import PatientDoctors from "../pages/patient/PatientDoctors.vue";
import PatientAppointments from "../pages/patient/PatientAppointments.vue";
import PatientHistory from "../pages/patient/PatientHistory.vue";




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
  { path: "/doctor/appointments", component: DoctorAppointments },
  { path: "/register", component: Register },
  { path: "/patient/doctors", component: PatientDoctors },
  { path: "/patient/appointments", component: PatientAppointments },
  { path: "/patient/history", component: PatientHistory },
  {path: "/admin/dashboard", component: AdminDashboard, meta: { requiresAuth: true, role: "admin" }},
  {path: "/doctor/dashboard", component: DoctorDashboard, meta: { requiresAuth: true, role: "doctor" }},
  {path: "/patient/dashboard", component: PatientDashboard, meta: { requiresAuth: true, role: "patient" }}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token")
  const role = localStorage.getItem("role")

  
  if (to.meta.requiresAuth && !token) {
    return next("/login")
  }

  
  if (to.path === "/login" && token) {
    if (role === "admin") return next("/admin/dashboard")
    if (role === "doctor") return next("/doctor/dashboard")
    if (role === "patient") return next("/patient/dashboard")
  }

  
  if (to.meta.role && role !== to.meta.role) {
    if (role === "admin") return next("/admin/dashboard")
    if (role === "doctor") return next("/doctor/dashboard")
    if (role === "patient") return next("/patient/dashboard")
  }

  next()
})
export default router;



