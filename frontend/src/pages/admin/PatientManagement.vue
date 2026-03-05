<script setup>
import { ref, computed, onMounted } from "vue"
import axios from "axios"

const patients = ref([])
const search = ref("")
const filterType = ref("name")

const token = localStorage.getItem("token")

/* Active / Blacklisted separation */

const activePatients = computed(() =>
  patients.value.filter(p => p.is_active)
)

const blacklistedPatients = computed(() =>
  patients.value.filter(p => !p.is_active)
)


/* Fetch patients */

const fetchPatients = async () => {
  try {

    const response = await axios.get(
      "http://127.0.0.1:5000/api/admin/patients",
      {
        headers: {
          "Authentication-Token": token
        },
        params: {
        name: filterType.value === "name" ? search.value : undefined,
        contact: filterType.value === "contact" ? search.value : undefined,
        patient_id: filterType.value === "id" ? search.value : undefined
        }
      }
    )

    patients.value = response.data

  } catch (error) {
    console.error(error)
  }
}


/* Blacklist patient */

const blacklistPatient = async (id) => {

  try {

    await axios.patch(
      `http://127.0.0.1:5000/api/admin/blacklist-patient/${id}`,
      {},
      {
        headers: {
          "Authentication-Token": token
        }
      }
    )

    fetchPatients()

  } catch (error) {
    console.error(error)
  }

}


/* Delete patient permanently */

const deletePatient = async (id) => {

  if (!confirm("Are you sure you want to permanently delete this patient?"))
    return

  try {

    await axios.delete(
      `http://127.0.0.1:5000/api/admin/delete-patient/${id}`,
      {
        headers: {
          "Authentication-Token": token
        }
      }
    )

    fetchPatients()

  } catch (error) {
    console.error(error)
    alert("Failed to delete patient")
  }

}


onMounted(() => {
  fetchPatients()
})

</script>


<template>

<div class="container mt-4">

<h2>Patient Management</h2>


<!-- Search Section -->

<div class="row mb-3">

<div class="col-md-3">

<select
v-model="filterType"
class="form-select"
>
<option value="name">Search by Name</option>
<option value="contact">Search by Phone</option>
<option value="id">Search by Patient ID</option>
</select>

</div>

<div class="col-md-9">

<input
v-model="search"
@input="fetchPatients"
class="form-control"
placeholder="Enter search value"
/>

</div>

</div>

<!-- Active Patients -->

<h4 class="mt-4">Active Patients</h4>

<table class="table table-bordered table-hover">

<thead class="table-light">

<tr>

<th>Name</th>
<th>Email</th>
<th>Gender</th>
<th>Blood Group</th>
<th>Contact</th>
<th>Action</th>

</tr>

</thead>


<tbody>

<tr v-for="p in activePatients" :key="p.patient_id">

<td>{{ p.name }}</td>
<td>{{ p.email }}</td>
<td>{{ p.gender }}</td>
<td>{{ p.blood_group }}</td>
<td>{{ p.contact_number }}</td>

<td>

<button
class="btn btn-sm btn-danger me-2"
@click="blacklistPatient(p.patient_id)"
>
Blacklist
</button>

<button
class="btn btn-sm btn-dark"
@click="deletePatient(p.patient_id)"
>
Delete
</button>

</td>

</tr>


<tr v-if="activePatients.length === 0">

<td colspan="6" class="text-center text-muted">
No active patients found
</td>

</tr>

</tbody>

</table>



<!-- Blacklisted Patients -->

<h4 class="mt-5 text-danger">Blacklisted Patients</h4>

<table class="table table-bordered table-hover">

<thead class="table-light">

<tr>

<th>Name</th>
<th>Email</th>
<th>Gender</th>
<th>Blood Group</th>
<th>Contact</th>
<th>Action</th>

</tr>

</thead>


<tbody>

<tr v-for="p in blacklistedPatients" :key="p.patient_id">

<td>{{ p.name }}</td>
<td>{{ p.email }}</td>
<td>{{ p.gender }}</td>
<td>{{ p.blood_group }}</td>
<td>{{ p.contact_number }}</td>

<td>

<button
class="btn btn-sm btn-dark"
@click="deletePatient(p.patient_id)"
>
Delete
</button>

</td>

</tr>


<tr v-if="blacklistedPatients.length === 0">

<td colspan="6" class="text-center text-muted">
No blacklisted patients
</td>

</tr>

</tbody>

</table>

</div>

</template>