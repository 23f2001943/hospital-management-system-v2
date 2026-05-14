<script setup>
import { ref, onMounted, computed } from "vue"
import API from "../../api"
const doctors = ref([])
const activeDoctors = computed(() =>
  doctors.value.filter(doc => doc.is_active)
)

const blacklistedDoctors = computed(() =>
  doctors.value.filter(doc => !doc.is_active)
)
const deleteDoctor = async (id) => {
  if (!confirm("Are you sure you want to permanently delete this doctor?")) {
    return
  }

  try {
    await API.delete(
      `/api/admin/delete-doctor/${id}`,
      {
        headers: {
          "Authentication-Token": token
        }
      }
    )

    fetchDoctors()

  } catch (error) {
    console.error(error)
    alert("Failed to delete doctor")
  }
}
const search = ref("")
const departments = ref([])
const showAddForm = ref(false)

const specialization = ref("")

const token = localStorage.getItem("token")
const newDoctor = ref({
  name: "",
  email: "",
  password: "",
  department_id: "",
  qualification: "",
  experience_years: "",
  consultation_fee: "",
  contact_number: "",
  room_number: "",
  availability: ""
})

const editingDoctor = ref(null)

const editDoctor = (doc) => {
  editingDoctor.value = { ...doc }
}

const updateDoctor = async () => {
  await API.put(
    `/api/admin/update-doctor/${editingDoctor.value.doctor_id}`,
    editingDoctor.value,
    {
      headers: {
        "Authentication-Token": token
      }
    }
  )

  editingDoctor.value = null
  fetchDoctors()
}

const addDoctor = async () => {
  try {
    await API.post(
      "/api/admin/add-doctor",
      newDoctor.value,
      {
        headers: {
          "Authentication-Token": token
        }
      }
    )

    // reset form
    newDoctor.value = {
        name: "",
        email: "",
        password: "",
        department_id: "",
        qualification: "",
        experience_years: "",
        consultation_fee: "",
        contact_number: "",
        room_number: "",
        availability: ""
        }
    showAddForm.value = false
    fetchDoctors()
  } catch (error) {
    console.error(error)
    alert("Failed to add doctor")
  }
}

const fetchDoctors = async () => {
  try {
    const response = await API.get(
      "/api/admin/doctors",
      {
        headers: {
          "Authentication-Token": token
        },
        params: {
            name: search.value || undefined,
            specialization: specialization.value || undefined
            }
      }
    )

    doctors.value = response.data
  } catch (error) {
    console.error(error)
  }

}

const blacklistDoctor = async (id) => {
  await API.patch(
    `/api/admin/blacklist-doctor/${id}`,
    {},
    {
      headers: {
        "Authentication-Token": token
      }
    }
  )
  fetchDoctors()
}

onMounted(() => {
  fetchDoctors()
})
const fetchDepartments = async () => {
  try {
    const response = await API.get(
      "/api/admin/departments",
      {
        headers: {
          "Authentication-Token": token
        }
      }
    )
    departments.value = response.data
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  fetchDoctors()
  fetchDepartments()
})

</script>

<template>
  <div class="container mt-4">
    <h2>Doctor Management</h2>
    <!--    search bar-->
    <div class="row mb-3">
    <div class="col-md-8">
        <input
        v-model="search"
        @input="fetchDoctors"
        class="form-control"
        placeholder="Search by name"
        />
    </div>

    <div class="col-md-4">
        <select
        v-model="specialization"
        @change="fetchDoctors"
        class="form-select"
        >
        <option value="">All Departments</option>
        <option
            v-for="dept in departments"
            :key="dept.id"
            :value="dept.id"
        >
            {{ dept.name }}
        </option>
        </select>
    </div>
    </div>

    <!-- Add Doctor Button -->
    <div class="mb-3">
    <button
        class="btn btn-primary"
        @click="showAddForm = !showAddForm"
    >
        {{ showAddForm ? "Close Form" : "+ Add Doctor" }}
    </button>
    </div>

    <!-- Collapsible Form -->
    <div v-if="showAddForm" class="card p-4 mb-4 shadow-sm">
    <h5 class="mb-3">Add New Doctor</h5>

    <div class="row g-3">
        <div class="col-md-6">
        <input v-model="newDoctor.name" class="form-control" placeholder="Name" />
        </div>

        <div class="col-md-6">
        <input v-model="newDoctor.email" class="form-control" placeholder="Email" />
        </div>

        <div class="col-md-6">
        <input v-model="newDoctor.password" type="password" class="form-control" placeholder="Password" />
        </div>

        <div class="col-md-6">
        <select v-model="newDoctor.department_id" class="form-select">
            <option value="">Select Department</option>
            <option
            v-for="dept in departments"
            :key="dept.id"
            :value="dept.id"
            >
            {{ dept.name }}
            </option>
        </select>
        </div>

        <div class="col-md-6">
        <input v-model="newDoctor.qualification" class="form-control" placeholder="Qualification" />
        </div>

        <div class="col-md-6">
        <input v-model="newDoctor.experience_years" type="number" class="form-control" placeholder="Experience (years)" />
        </div>

        <div class="col-md-6">
        <input v-model="newDoctor.consultation_fee" type="number" class="form-control" placeholder="Consultation Fee" />
        </div>

        <div class="col-md-6">
        <input v-model="newDoctor.contact_number" class="form-control" placeholder="Contact Number" />
        </div>

        <div class="col-md-6">
        <input v-model="newDoctor.room_number" class="form-control" placeholder="Room Number" />
        </div>

        <div class="col-md-6">
        <input v-model="newDoctor.availability" class="form-control" placeholder='Availability JSON e.g {"Mon":"9-5"}' />
        </div>

        <div class="col-12 text-end">
        <button class="btn btn-success px-4" @click="addDoctor">
            Save Doctor
        </button>
        </div>
    </div>
    </div>

    <div v-if="editingDoctor" class="card p-3 mt-4">
        <h5>Edit Doctor</h5>

        <input v-model="editingDoctor.department_id" class="form-control mb-2" placeholder="Dept ID" />
        <input v-model="editingDoctor.qualification" class="form-control mb-2" placeholder="Qualification" />
        <input v-model="editingDoctor.experience_years" class="form-control mb-2" placeholder="Experience" />
        <input v-model="editingDoctor.consultation_fee" class="form-control mb-2" placeholder="Fee" />
        <input v-model="editingDoctor.contact_number" class="form-control mb-2" placeholder="Contact" />
        <input v-model="editingDoctor.room_number" class="form-control mb-2" placeholder="Room Number" />
        <input v-model="editingDoctor.availability" class="form-control mb-2" placeholder="Availability JSON" />

        <button class="btn btn-success" @click="updateDoctor">
            Save Changes
        </button>
    </div>

    <!--active doctors -->
    <h4 class="mt-4">Active Doctors</h4>

    <table class="table table-bordered table-hover">
    <thead class="table-light">
        <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Department</th>
        <th>Experience</th>
        <th>Fee</th>
        <th>Action</th>
        </tr>
    </thead>
    <tbody>
        <tr v-for="doc in activeDoctors" :key="doc.doctor_id">
        <td>{{ doc.name }}</td>
        <td>{{ doc.email }}</td>
        <td>{{ doc.department }}</td>
        <td>{{ doc.experience_years }}</td>
        <td>{{ doc.consultation_fee }}</td>
        <td>
            <button
            class="btn btn-sm btn-warning me-2"
            @click="editDoctor(doc)"
            >
            Edit
            </button>

            <button
            class="btn btn-sm btn-dark"
            @click="deleteDoctor(doc.doctor_id)"
            >
            Delete
            </button>

            <button
            class="btn btn-sm btn-danger"
            @click="blacklistDoctor(doc.doctor_id)"
            >
            Blacklist
            </button>
        </td>
        </tr>

        <tr v-if="activeDoctors.length === 0">
        <td colspan="6" class="text-center text-muted">
            No active doctors found
        </td>
        </tr>
    </tbody>
    </table>
<!--        blacklisted doctors-->
        <h4 class="mt-5 text-danger">Blacklisted Doctors</h4>

        <table class="table table-bordered table-hover">
        <thead class="table-light">
            <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Department</th>
            <th>Experience</th>
            <th>Fee</th>
            <th>Action</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="doc in blacklistedDoctors" :key="doc.doctor_id">
            <td>{{ doc.name }}</td>
            <td>{{ doc.email }}</td>
            <td>{{ doc.department }}</td>
            <td>{{ doc.experience_years }}</td>
            <td>{{ doc.consultation_fee }}</td>
            <td>
                <button
                class="btn btn-sm btn-warning"
                @click="editDoctor(doc)"
                >
                Edit
                </button>

                <button
                class="btn btn-sm btn-dark ms-2"
                @click="deleteDoctor(doc.doctor_id)"
                >
                Delete
                </button>
            </td>
            </tr>

            <tr v-if="blacklistedDoctors.length === 0">
            <td colspan="6" class="text-center text-muted">
                No blacklisted doctors
            </td>
            </tr>
        </tbody>
        </table>
            
  </div>
</template>
