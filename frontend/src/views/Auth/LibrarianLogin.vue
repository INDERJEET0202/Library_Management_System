<template>
  <div>
    <AuthNavbar />
    <div class="container">
      <h1 class="header">Librarian Login</h1>
      <form>
        <div class="mb-3">
          <label for="exampleInputEmail1" class="form-label"
            >Email address</label
          >
          <input
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
            type="password"
            class="form-control"
            id="exampleInputPassword1"
          />
        </div>
        <div class="button">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import AuthNavbar from "../../components/AuthNavbar/AuthNavbar.vue";

export default {
  name: "LibrarianLogin",
  components: {
    AuthNavbar,
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
</style>