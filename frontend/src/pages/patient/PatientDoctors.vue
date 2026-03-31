<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

// STATE
const doctors = ref([])
const searchName = ref("")
const specialization = ref("")

const availability = ref([])
const expandedDoctorId = ref(null)

const selectedSlot = ref(null)

const viewDoctorId = ref(null)
const toggleView = (doc) => {
  if (viewDoctorId.value === doc.doctor_id) {
    viewDoctorId.value = null
  } else {
    viewDoctorId.value = doc.doctor_id
  }
}

const bookAppointment = async () => {

  if (!selectedSlot.value) {
    alert("Please select a slot")
    return
  }

  try {
    await axios.post(
      "http://127.0.0.1:5000/api/patient/book",
      {
        doctor_id: expandedDoctorId.value,
        date: selectedSlot.value.date,
        time: selectedSlot.value.time
      },
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    alert("Appointment booked!")

    // reset
    selectedSlot.value = null
    expandedDoctorId.value = null

  } catch (err) {
    alert(err.response?.data?.message || "Error booking")
  }
}

// ================= FETCH DOCTORS =================
const fetchDoctors = async () => {
  try {
    const res = await axios.get(
      "http://127.0.0.1:5000/api/patient/doctors",
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
    console.error(err.response?.data || err)
  }
}

// ================= FETCH AVAILABILITY =================
const fetchAvailability = async (doctorId) => {
  try {
    const res = await axios.get(
      `http://127.0.0.1:5000/api/patient/doctor/${doctorId}/availability`,
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    availability.value = res.data

  } catch (err) {
    console.error(err)
  }
}

// ================= OPEN / CLOSE =================
const openBooking = (doc) => {

  if (expandedDoctorId.value === doc.doctor_id) {
    expandedDoctorId.value = null
    return
  }

  expandedDoctorId.value = doc.doctor_id
  fetchAvailability(doc.doctor_id)
}

// ================= LIFECYCLE =================
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
               placeholder="Search by department" />
      </div>

      <div class="col-md-2">
        <button class="btn btn-primary w-100"
                @click="fetchDoctors">
          Search
        </button>
      </div>

    </div>

    <!-- TABLE -->
    <table class="table table-bordered">

      <thead>
        <tr>
          <th>Name</th>
          <th>Department</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <template v-for="doc in doctors" :key="doc.doctor_id">

          <!-- MAIN ROW -->
          <tr>
            <td>{{ doc.name }}</td>
            <td>{{ doc.department }}</td>
            <td>

                <button class="btn btn-info btn-sm me-2"
                        @click="toggleView(doc)">
                    View
                </button>
              <button class="btn btn-success btn-sm"
                      @click="openBooking(doc)">
                Book
              </button>
            </td>
          </tr>

          <!-- VIEW DETAILS ROW -->
            <tr v-if="viewDoctorId === doc.doctor_id">
            <td colspan="3">

                <div class="card p-3 shadow-sm bg-light">

                <h5>Doctor Details</h5>

                <p><b>Name:</b> {{ doc.name }}</p>
                <p><b>Department:</b> {{ doc.department }}</p>
                <p><b>Qualification:</b> {{ doc.qualification || '-' }}</p>
                <p><b>Experience:</b> {{ doc.experience_years || '-' }} years</p>
                <p><b>Consultation Fee:</b> ₹{{ doc.consultation_fee || '-' }}</p>
                <p><b>Contact:</b> {{ doc.contact_number || '-' }}</p>
                <p><b>Room:</b> {{ doc.room_number || '-' }}</p>

                </div>

            </td>
            </tr>

          <!-- EXPANDED ROW -->
          <tr v-if="expandedDoctorId === doc.doctor_id">
            <td colspan="3">

              <div class="card p-3 shadow-sm">

                <h5>Doctor Availability</h5>

                <div v-if="availability.length === 0">
                  No availability set
                </div>

                <div v-for="day in availability" :key="day.date"
                     class="d-flex align-items-center mb-2">

                  <!-- DATE -->
                  <div style="width: 150px;">
                    <b>{{ day.date }}</b>
                  </div>

                    <!-- MORNING -->
                    <button class="btn me-2"
                            :class="[
                            day.morning ? 'btn-success' : 'btn-outline-secondary',
                            selectedSlot?.date === day.date && selectedSlot?.time === '09:00' ? 'btn-warning' : ''
                            ]"
                            :disabled="!day.morning"
                            @click="selectedSlot = { date: day.date, time: '09:00' }">
                    08:00 - 12:00
                    </button>

                    <!-- EVENING -->
                    <button class="btn"
                            :class="[
                            day.evening ? 'btn-success' : 'btn-outline-secondary',
                            selectedSlot?.date === day.date && selectedSlot?.time === '17:00' ? 'btn-warning' : ''
                            ]"
                            :disabled="!day.evening"
                            @click="selectedSlot = { date: day.date, time: '17:00' }">
                    16:00 - 21:00
                    </button>

                </div>
                <div class="mt-3">

                <button class="btn btn-primary btn-sm me-2"
                        :disabled="!selectedSlot"
                        @click="bookAppointment">
                    Submit
                </button>

                </div>

              </div>

            </td>
          </tr>

        </template>

      </tbody>

    </table>

  </div>
</template>