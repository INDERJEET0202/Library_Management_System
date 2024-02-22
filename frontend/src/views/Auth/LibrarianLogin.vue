<template>
  <div>
    <AuthNavbar />
    <div class="container">
      <h1 class="header">Librarian Login</h1>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="exampleInputEmail1" class="form-label"
            >Email address</label
          >
          <input
            v-model="email"
            type="email"
            class="form-control"
            id="exampleInputEmail1"
            aria-describedby="emailHelp"
          />
          <div id="emailHelp" class="form-text">
            We'll never share your email with anyone else.
          </div>
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            id="exampleInputPassword1"
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
import AuthNavbar from "../../components/AuthNavbar/AuthNavbar.vue";
import axios from "axios";

export default {
  name: "LibrarianLogin",
  components: {
    AuthNavbar,
  },
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    login() {
      axios
        .post("http://127.0.0.1:5000/api/librarian/login", {
          email: this.email,
          password: this.password,
        })
        .then((response) => {
          const { access_token } = response.data;
          localStorage.setItem("accessToken", access_token);
          localStorage.setItem("userType", "librarian");
          console.log(
            "Librarian logged in successfully.",
          );
          // Redirect or perform any other actions upon successful login
          this.$router.push("/librarian/dashboard");
        })
        .catch((error) => {
          this.errorMessage = error.response.data.error;
          console.error(
            "Error logging in as librarian:",
            error.response.data.error
          );
        });
    },
  },
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
