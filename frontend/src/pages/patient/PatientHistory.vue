<script setup>
import { ref, onMounted } from "vue"
import API from "../../api"
const history = ref([])

const fetchHistory = async () => {
  try {
    const res = await API.get(
      "/api/patient/history",
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    history.value = res.data

  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchHistory)
</script>

<template>
  <div class="container mt-4">

    <h2 class="mb-4">Medical History</h2>

    <table class="table table-bordered">

      <thead>
        <tr>
          <th>Doctor</th>
          <th>Department</th>
          <th>Date</th>
          <th>Time</th>
          <th>Status</th>
          <th>Diagnosis</th>
          <th>Prescription</th>
          <th>Notes</th>
        </tr>
      </thead>

      <tbody>

        <tr v-for="h in history" :key="h.date + h.time">

          <td>{{ h.doctor_name }}</td>
          <td>{{ h.department }}</td>
          <td>{{ h.date }}</td>

          <td>
            {{ h.time === '09:00' ? '08:00 - 12:00' : '16:00 - 21:00' }}
          </td>

          <td>{{ h.status }}</td>

          <td>{{ h.diagnosis || '-' }}</td>
          <td>{{ h.prescription || '-' }}</td>
          <td>{{ h.notes || '-' }}</td>

        </tr>

      </tbody>

    </table>

  </div>
</template>
