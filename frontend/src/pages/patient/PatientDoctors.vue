<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

const doctors = ref([])
const searchName = ref("")
const specialization = ref("")

// fetch doctors
const fetchDoctors = async () => {
  try {
    const res = await axios.get(
      `http://127.0.0.1:5000/api/patient/doctors`,
      {
        params: {
          name: searchName.value,
          specialization: specialization.value
        },
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    doctors.value = res.data

  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchDoctors)
</script>

<template>
  <div class="container mt-4">

    <h2 class="mb-4">Doctors</h2>

    <!-- SEARCH -->
    <div class="row mb-3">

      <div class="col-md-4">
        <input v-model="searchName"
               class="form-control"
               placeholder="Search by name" />
      </div>

      <div class="col-md-4">
        <input v-model="specialization"
               class="form-control"
               placeholder="Search by department ID" />
      </div>

      <div class="col-md-2">
        <button class="btn btn-primary w-100"
                @click="fetchDoctors">
          Search
        </button>
      </div>

    </div>

    <!--  TABLE -->
    <table class="table table-bordered">

      <thead>
        <tr>
          <th>Name</th>
          <th>Department</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="doc in doctors" :key="doc.doctor_id">
          <td>{{ doc.name }}</td>
          <td>{{ doc.department }}</td>
        </tr>
      </tbody>

    </table>

  </div>
</template>