<template>
  <div class="container mt-5">
    <h2>Register</h2>

    <input v-model="name" class="form-control mb-2" placeholder="Name" />
    <input v-model="email" class="form-control mb-2" placeholder="Email" />
    <input v-model="password" type="password" class="form-control mb-2" placeholder="Password" />

    <button class="btn btn-success" @click="register">Register</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: ""
    };
  },
  methods: {
    async register() {
      try {
        await axios.post("http://127.0.0.1:5000/auth/register", {
          name: this.name,
          email: this.email,
          password: this.password
        });

        alert("Registered successfully");
        this.$router.push("/login");

      } catch {
        alert("Registration failed");
      }
    }
  }
};
</script>