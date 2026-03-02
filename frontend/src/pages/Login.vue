<template>
  <div class="container mt-5">
    <h2>Login</h2>

    <input v-model="email" class="form-control mb-2" placeholder="Email" />
    <input v-model="password" type="password" class="form-control mb-2" placeholder="Password" />

    <button class="btn btn-primary" @click="login">Login</button>
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
    async login() {
      try {
        const res = await axios.post("http://127.0.0.1:5000/auth/login", {
          email: this.email,
          password: this.password
        });

        localStorage.setItem("token", res.data.token);

        const role = res.data.roles[0];
        if (role === "admin") this.$router.push("/admin");
        else if (role === "doctor") this.$router.push("/doctor");
        else this.$router.push("/patient");

      } catch {
        alert("Invalid login");
      }
    }
  }
};
</script>