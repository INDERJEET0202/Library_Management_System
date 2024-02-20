<template>
  <div>
    <AuthNavbar />
    <div class="container">
      <h1 class="header">User Signup</h1>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="exampleInputName" class="form-label">Username</label>
          <input
            type="text"
            class="form-control"
            id="exampleInputName"
            v-model="name"
          />
        </div>
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
          <div id="emailHelp" class="form-text">
            <small>We'll never share your email with anyone else.</small>
          </div>
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="InputPassword1"
            v-model="password"
          />
        </div>
        <div class="mb-3">
          <label for="ConfirmPassword1" class="form-label"
            >Confirm Password</label
          >
          <input
            type="password"
            class="form-control"
            id="exampleInputPassword1"
            v-model="confirmPassword"
          />
        </div>
        <div class="mb-3 form-check">
          <input
            type="checkbox"
            class="form-check-input"
            id="exampleCheck1"
            v-model="agreedToTerms"
          />
          <label class="form-check-label" for="exampleCheck1"
            >I agree to Terms and Conditions</label
          >
        </div>
        <div class="button">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
        <div class="already-have-account">
          <small class="mt-3">
            Already have an account?
            <router-link to="/userlogin">Login</router-link>
          </small>
        </div>
      </form>
    </div>
  </div>
</template>
  
  <script>
import AuthNavbar from "../../components/AuthNavbar/AuthNavbar.vue";
import DOMPurify from "dompurify";
import axios from "axios";
// import cors from "cors";
// import bcrypt from "bcryptjs";

export default {
  name: "UserSignup",
  components: {
    AuthNavbar,
  },
  data() {
    return {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
      agreedToTerms: false,
    };
  },
  methods: {
    submitForm() {
      // Sanitize data
      const sanitizedName = this.sanitizeInput(this.name);
      const sanitizedEmail = this.sanitizeInput(this.email);
      const sanitizedPassword = this.sanitizeInput(this.password);
      // const sanitizedConfirmPassword = this.sanitizeInput(this.confirmPassword);
      // const hashedPassword = bcrypt.hashSync(sanitizedPassword, 10);
      if (!this.validateData()) {
        return;
      }

      axios
        .post("http://127.0.0.1:5000/api/signup", {
          name: sanitizedName,
          email: sanitizedEmail,
          password: sanitizedPassword,
        })
        .then((response) => {
          console.log("Response from Flask backend:", response.data.message);
          this.$router.push('/userlogin');
        })
        .catch((error) => {
          if (error.response && error.response.status === 400) {
            alert(error.response.data.error);
          } else {
            alert("Some error occurred, please try again later");
            console.error("Error:", error);
          }
        });
    },
    // purification
    sanitizeInput(input) {
      return DOMPurify.sanitize(input);
    },
    // validation
    validateData() {
      if (
        this.name === "" ||
        this.email === "" ||
        this.password === "" ||
        this.confirmPassword === ""
      ) {
        alert("Please fill in all fields");
        return false;
      }
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match");
        return false;
      }
      if (!this.agreedToTerms) {
        alert("Please agree to terms and conditions");
        return false;
      }
      return true;
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

.already-have-account {
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}
</style>