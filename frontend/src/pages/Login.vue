<template>
  <div class="container mt-5">
    <h2>Login</h2>

    <input v-model="email" class="form-control mb-2" placeholder="Email" />
    <input v-model="password" type="password" class="form-control mb-2" placeholder="Password" />

    <button class="btn btn-primary" @click="login">Login</button>

    <div class="mt-3">
      <span>Don't have an account?</span>
      <span 
        style="color: blue; cursor: pointer; margin-left: 5px;"
        @click="goToRegister"
      >
        Register
      </span>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      password: ""
    };
  },
  methods: {
    goToRegister() {
      this.$router.push("/register");
    },



    async login() {
      try {
        const res = await axios.post("http://127.0.0.1:5000/auth/login", {
          email: this.email,
          password: this.password
        });

        localStorage.setItem("token", res.data.token);

        const role = res.data.roles[0];
        localStorage.setItem("role", role);
        if (role === "admin") this.$router.push("/admin/dashboard");
        else if (role === "doctor") this.$router.push("/doctor/dashboard");
        else this.$router.push("/patient/dashboard");

      } catch {
        alert("Invalid login");
      }
    }
  }
};
</script>