<template>
  <div>
    <div class="container">
      <h1 class="header">Admin Login</h1>
      <form @submit.prevent="loginUser">
        <div class="mb-3">
          <label for="exampleInputEmail1" class="form-label"
            >Email address</label
          >
          <input
            type="email"
            class="form-control"
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
            v-model="email"
          />
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="exampleInputPassword1"
            v-model="password"
          />
        </div>
        <div class="button">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
        <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AdminLogin",
  data(){
    return {
      email: "",
      password: "",
      errorMessage: "",
    }
  },
  methods: {
    async loginUser(){
        try{
            const response = await axios.post("http://127.0.0.1:5000/api/admin/login", {
                email: this.email,
                password: this.password,
            });
            if(response.data.access_token){
                localStorage.setItem("accessToken", response.data.access_token);
                localStorage.setItem("admin_name", response.data.admin_name);
                localStorage.setItem("userType", "admin");
                this.$router.push("/admin/dashboard");
            }
            } catch (error) {
            console.error("Error in logging in", error);
            this.errorMessage = error.response.data.error;
        }
    }
  }
};
</script>

<style scoped>
.container {
  width: 40%;
  margin-top: 50px;
  border: 1px solid rgb(165, 165, 165);
  border-radius: 10px;
  padding: 20px;
  font-family: Poppins, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 20px;
}

.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin-top: 15px;
  width: 30%;
  padding: 10px;
  border-radius: 10px;
  background-color: #54a7ff;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

.button {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>