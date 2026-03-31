<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

// STATE
const profile = ref({})
const editMode = ref(false)

// ================= FETCH PROFILE =================
const fetchProfile = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:5000/api/patient/profile",
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    profile.value = res.data

  } catch (err) {
    console.error(err)
  }
}

// ================= UPDATE PROFILE =================
const updateProfile = async () => {
  try {
    await axios.put(
      "http://127.0.0.1:5000/api/patient/profile",
      profile.value,
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    alert("Profile updated")
    editMode.value = false

  } catch (err) {
    console.error(err)
  }
}

// ================= LIFECYCLE =================
onMounted(fetchProfile)
</script>

<template>
  <div class="container mt-4">

    <!-- 🔷 NAVBAR -->
    <div class="d-flex justify-content-between align-items-center border p-3 mb-4">
      <h4>Welcome {{ profile.name }}</h4>

      <button class="btn btn-primary btn-sm"
              @click="editMode = !editMode">
        Edit Profile
      </button>
    </div>

    <!-- 🔷 EDIT PROFILE BOX -->
    <div v-if="editMode" class="card p-4 shadow-sm">

      <h5 class="mb-3">Edit Profile</h5>

      <!-- NAME -->
      <div class="mb-2">
        <label>Name</label>
        <input v-model="profile.name" class="form-control" />
      </div>

      <!-- GENDER -->
      <div class="mb-2">
        <label>Gender</label>
        <select v-model="profile.gender" class="form-control">
          <option value="">Select</option>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>

      <!-- BLOOD GROUP -->
      <div class="mb-2">
        <label>Blood Group</label>
        <input v-model="profile.blood_group" class="form-control" />
      </div>

      <!-- CONTACT -->
      <div class="mb-2">
        <label>Contact Number</label>
        <input v-model="profile.contact_number" class="form-control" />
      </div>

      <!-- EMERGENCY CONTACT -->
      <div class="mb-2">
        <label>Emergency Contact</label>
        <input v-model="profile.emergency_contact" class="form-control" />
      </div>

      <!-- ADDRESS -->
      <div class="mb-2">
        <label>Address</label>
        <textarea v-model="profile.address" class="form-control"></textarea>
      </div>

      <!-- DOB -->
      <div class="mb-3">
        <label>Date of Birth</label>
        <input type="date" v-model="profile.date_of_birth" class="form-control" />
      </div>

      <!-- ACTION BUTTONS -->
      <div class="d-flex justify-content-between mt-3">

        <button class="btn btn-success btn-sm"
                @click="updateProfile">
          Save
        </button>

        <button class="btn btn-secondary btn-sm"
                @click="editMode = false">
          Cancel
        </button>

      </div>

    </div>

  </div>
</template>