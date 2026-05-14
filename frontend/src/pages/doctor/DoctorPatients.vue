<script setup>
import { ref, onMounted } from "vue"
import API from "../../api";

const expandedPatientId = ref(null)
const patientHistory = ref({})
const assignedPatients = ref([])
const pastPatients = ref([])
// Fetch all patients
const fetchPatients = async () => {
  try {
    const res = await API.get("/api/doctor/patients", {
      headers: {
        "Authentication-Token": localStorage.getItem("token")
      }
    })

    assignedPatients.value = res.data.assigned
    pastPatients.value = res.data.past

  } catch (err) {
    console.error(err)
  }
}

// Fetch history of selected patient
const fetchHistory = async (id) => {
  try {
    const res = await API.get(
      `/api/doctor/patient/${id}/history`,
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    patientHistory.value[id] = res.data

  } catch (err) {
    console.error(err)
  }
}

// Toggle expand/collapse
const toggleView = (id) => {
  if (expandedPatientId.value === id) {
    expandedPatientId.value = null
  } else {
    expandedPatientId.value = id
    fetchHistory(id)
  }
}

onMounted(fetchPatients)
</script>

<template>
  <div class="container mt-4">

    <h4 class="mt-4">Assigned Patients</h4>

    <table class="table table-bordered">
    <thead>
        <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Action</th>
        </tr>
    </thead>

    <tbody>
        <template v-for="p in assignedPatients" :key="p.patient_id">

        <tr>
            <td>{{ p.name }}</td>
            <td>{{ p.email }}</td>
            <td>
            <button class="btn btn-primary btn-sm"
                    @click="toggleView(p.patient_id)">
                {{ expandedPatientId === p.patient_id ? "Close" : "View" }}
            </button>
            </td>
        </tr>

        <tr v-if="expandedPatientId === p.patient_id">
            <td colspan="3">
            <!-- SAME EXPANDED CARD (NO CHANGE) -->
            <div class="card p-3 shadow-sm">
                <!-- reuse your history UI -->
                <div class="d-flex justify-content-between">
                <h5>Patient History</h5>
                <button class="btn btn-secondary btn-sm"
                        @click="expandedPatientId = null">
                    Close
                </button>
                </div>

                <hr>

                <p><b>Name:</b> {{ p.name }}</p>
                <p><b>Email:</b> {{ p.email }}</p>
                <p><b>Contact:</b> {{ p.contact }}</p>

                <div v-if="!patientHistory[p.patient_id]">
                Loading history...
                </div>

                <table v-else class="table table-bordered mt-3">
                <thead>
                    <tr>
                    <th>Date</th>
                    <th>Time</th>
                    <th>Doctor</th>
                    <th>Department</th>
                    <th>Status</th>
                    <th>Diagnosis</th>
                    <th>Prescription</th>
                    <th>Notes</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="h in patientHistory[p.patient_id]" :key="h.appointment_id">
                    <td>{{ h.date }}</td>
                    <td>{{ h.time }}</td>
                    <td>{{ h.doctor_name }}</td>
                    <td>{{ h.department }}</td>
                    <td>{{ h.status }}</td>
                    <td>{{ h.diagnosis || '-' }}</td>
                    <td>{{ h.prescription || '-' }}</td>
                    <td>{{ h.notes || '-' }}</td>
                    </tr>
                </tbody>
                </table>
            </div>
            </td>
        </tr>

        </template>
    </tbody>
    </table>
    <h4 class="mt-5">Past Patients</h4>

<table class="table table-bordered">
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Action</th>
    </tr>
  </thead>

  <tbody>
    <template v-for="p in pastPatients" :key="p.patient_id">

      <tr>
        <td>{{ p.name }}</td>
        <td>{{ p.email }}</td>
        <td>
          <button class="btn btn-primary btn-sm"
                  @click="toggleView(p.patient_id)">
            {{ expandedPatientId === p.patient_id ? "Close" : "View" }}
          </button>
        </td>
      </tr>

      <tr v-if="expandedPatientId === p.patient_id">
        <td colspan="3">

          <!-- SAME EXPANDED CARD -->
          <div class="card p-3 shadow-sm">

            <div class="d-flex justify-content-between">
              <h5>Patient History</h5>
              <button class="btn btn-secondary btn-sm"
                      @click="expandedPatientId = null">
                Close
              </button>
            </div>

            <hr>

            <p><b>Name:</b> {{ p.name }}</p>
            <p><b>Email:</b> {{ p.email }}</p>
            <p><b>Contact:</b> {{ p.contact }}</p>

            <div v-if="!patientHistory[p.patient_id]">
              Loading history...
            </div>

            <table v-else class="table table-bordered mt-3">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Doctor</th>
                  <th>Department</th>
                  <th>Status</th>
                  <th>Diagnosis</th>
                  <th>Prescription</th>
                  <th>Notes</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="h in patientHistory[p.patient_id]" :key="h.appointment_id">
                  <td>{{ h.date }}</td>
                  <td>{{ h.time }}</td>
                  <td>{{ h.doctor_name }}</td>
                  <td>{{ h.department }}</td>
                  <td>{{ h.status }}</td>
                  <td>{{ h.diagnosis || '-' }}</td>
                  <td>{{ h.prescription || '-' }}</td>
                  <td>{{ h.notes || '-' }}</td>
                </tr>
              </tbody>
            </table>

          </div>

        </td>
      </tr>

    </template>
  </tbody>
</table>

  </div>
</template>
