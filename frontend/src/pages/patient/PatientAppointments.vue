<script setup>
import { ref, onMounted } from "vue"
import API from "../../api"
const appointments = ref([])

const expandedId = ref(null)
const availability = ref([])
const selectedSlot = ref(null)
const today = new Date()
today.setHours(0,0,0,0)

// FETCH
const fetchAppointments = async () => {
  try {
    const res = await API.get(
      "/api/patient/appointments",
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    const today = new Date()
    today.setHours(0, 0, 0, 0)

    appointments.value = res.data.filter(a => {
      const parts = a.date.split("-")   // ["2026","03","31"]

      const apptDate = new Date(
        Number(parts[0]),
        Number(parts[1]) - 1,
        Number(parts[2])
      )

      return apptDate >= today
    })

  } catch (err) {
    console.error(err)
  }
}

// CANCEL
const cancelAppointment = async (id) => {
  try {
    await API.patch(
      `/api/patient/appointment/${id}/cancel`,
      {},
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    fetchAppointments()

  } catch (err) {
    console.error(err)
  }
}

// RESCHEDULE 
const rescheduleAppointment = async (appt) => {

  if (expandedId.value === appt.appointment_id) {
    expandedId.value = null
    return
  }

  expandedId.value = appt.appointment_id
  selectedSlot.value = null

  try {
    const res = await API.get(
      `/api/patient/doctor/${appt.doctor_id}/availability`,
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

const submitReschedule = async (appt) => {

  if (!selectedSlot.value) {
    alert("Select a slot")
    return
  }

  try {
    await API.put(
      `/api/patient/appointment/${appt.appointment_id}/reschedule`,
      {
        date: selectedSlot.value.date,
        time: selectedSlot.value.time
      },
      {
        headers: {
          "Authentication-Token": localStorage.getItem("token")
        }
      }
    )

    alert("Rescheduled successfully")

    expandedId.value = null
    selectedSlot.value = null

    fetchAppointments()

  } catch (err) {
    alert(err.response?.data?.message || "Error")
  }
}

onMounted(fetchAppointments)
</script>

<template>
  <div class="container mt-4">

    <h2 class="mb-4">Upcoming Appointments</h2>

    <table class="table table-bordered">

      <thead>
        <tr>
          <th>Doctor</th>
          <th>Department</th>
          <th>Date</th>
          <th>Time</th>
          <th>Status</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>

        <template v-for="a in appointments" :key="a.appointment_id">

        <tr>
        <td>{{ a.doctor_name }}</td>
        <td>{{ a.department }}</td>
        <td>{{ a.date }}</td>
        <td>{{ a.time === '09:00' ? '08:00 - 12:00' : '16:00 - 21:00' }}</td>
        <td>
            <span
            :class="[
                'badge',
                a.status === 'Booked' ? 'bg-success' :
                a.status === 'Cancelled' ? 'bg-danger' :
                'bg-secondary'
            ]"
            >
            {{ a.status }}
            </span>
        </td>
        <td>
            <button class="btn btn-danger btn-sm me-2"
                    :disabled="a.status === 'Cancelled'"
                    @click="cancelAppointment(a.appointment_id)">
            Cancel
            </button>

            <button class="btn btn-warning btn-sm"
                    :disabled="a.status === 'Cancelled'"
                    @click="rescheduleAppointment(a)">
            Reschedule
            </button>
        </td>
        </tr>

        <!-- EXPANDED ROW -->
        <tr v-if="expandedId === a.appointment_id">
        <td colspan="5">

            <div class="card p-3 shadow-sm">

            <h5>Reschedule Appointment</h5>

            <div v-for="day in availability" :key="day.date"
                class="d-flex align-items-center mb-2">

                <div style="width: 150px;">
                <b>{{ day.date }}</b>
                </div>

                <!-- MORNING -->
                <button class="btn me-2"
                        :class="[
                        day.morning ? 'btn-success' : 'btn-outline-secondary',
                        selectedSlot?.date === day.date && selectedSlot?.time === '09:00'
                            ? 'btn-warning'
                            : ''
                        ]"
                        :disabled="!day.morning"
                        @click="selectedSlot = {
                        date: day.date,
                        time: '09:00',
                        label: '08:00 - 12:00'
                        }">
                08:00 - 12:00
                </button>

                <!-- EVENING -->
                <button class="btn"
                        :class="[
                        day.evening ? 'btn-success' : 'btn-outline-secondary',
                        selectedSlot?.date === day.date && selectedSlot?.time === '17:00'
                            ? 'btn-warning'
                            : ''
                        ]"
                        :disabled="!day.evening"
                        @click="selectedSlot = {
                        date: day.date,
                        time: '17:00',
                        label: '16:00 - 21:00'
                        }">
                16:00 - 21:00

                </button>

            </div>

            <button class="btn btn-primary btn-sm mt-2"
                    :disabled="!selectedSlot"
                    @click="submitReschedule(a)">
                Submit
            </button>

            </div>

        </td>
        </tr>

        </template>

      </tbody>

    </table>

  </div>
</template>
