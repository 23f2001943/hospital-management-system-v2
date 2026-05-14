<template>
  <div class="container mt-5">
    <h2>Register</h2>

    <input v-model="name" class="form-control mb-2" placeholder="Name" />
    <input v-model="email" class="form-control mb-2" placeholder="Email" />
    <input v-model="password" type="password" class="form-control mb-2" placeholder="Password" />

    <button class="btn btn-success" @click="register">Register</button>
    <div class="mt-3">
    <span>Already have an account?</span>
    <span 
      style="color: blue; cursor: pointer; margin-left: 5px;"
      @click="goToLogin"
    >
      Login
    </span>
  </div>
  </div>
</template>

<script>
import API from "../api";

export default {
  data() {
    return {
      name: "",
      email: "",
      password: ""
    };
  },
  methods: {
    goToLogin() {
  this.$router.push("/login");
},
    async register() {
      try {
        await API.post("/auth/register", {
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
