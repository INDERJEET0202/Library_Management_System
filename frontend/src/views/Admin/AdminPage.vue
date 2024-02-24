<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#"
          >Welcome to admin page, {{ admin_name }}</a
        >
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </div>
    </nav>
    <div class="container">
      <table class="table">
        <caption>
          List of all users
        </caption>
        <thead>
          <tr>
            <th scope="col">ID</th>
            <th scope="col">Name</th>
            <th scope="col">Email</th>
            <th scope="col">Role</th>
            <th scope="col">Change Role</th>
            <th scope="col">Delete User</th>
          </tr>
        </thead>
        <tbody>
          <!-- Loop through users and render each user -->
          <tr v-for="(user, index) in users" :key="index">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>
              <select v-model="user.role" @change="updateUserRole(user)">
                <option v-for="role in roles" :value="role" :key="role">
                  {{ role }}
                </option>
              </select>
            </td>
            <td>
              <button class="delete_btn" @click="deleteUser(user.id)">
                Delete
                <i
                  class="fa fa-trash-o"
                  style="font-size: 20px; color: rgb(255, 56, 56)"
                ></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "AdminPage",
  data() {
    return {
      users: [],
      admin_name: "",
      roles: ["user", "admin", "librarian"],
      errorMessage: "",
    };
  },
  mounted() {
    this.getUsers();
    this.admin_name = localStorage.getItem("admin_name");
  },
  methods: {
    async saveRoles() {},
    logout() {
      localStorage.removeItem("accessToken");
      localStorage.removeItem("admin_name");
      localStorage.removeItem("userType");
      this.$router.push("/adminlogin");
    },
    async getUsers() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/admin/users",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          this.users = response.data;
        } else {
          // Handle error responses
          console.error("Error fetching users:", response.data.error);
        }
      } catch (error) {
        console.error("Error fetching users:", error);
        this.errorMessage = "Session expired. Please login again.";
      }
    },
    async updateUserRole(user) {
      try {
        // console.log(user.role)
        const response = await axios.put(
          `http://127.0.0.1:5000/api/admin/users/${user.id}/role`,
          { role: user.role },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          console.log(response.data.message);
        } else {
          console.error("Error updating user role:", response.data.error);
        }
      } catch (error) {
        console.error("Error updating user role:", error);
        this.errorMessage = error.response.data.error;
      }
    },
    async deleteUser(userId) {
      try {
        const response = await axios.delete(
          `http://127.0.0.1:5000/api/admin/users/${userId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          console.log("User deleted successfully");
          // Remove the user from the local list
          this.users = this.users.filter((user) => user.id !== userId);
        } else {
          console.error("Error deleting user:", response.data.error);
        }
      } catch (error) {
        console.error("Error deleting user:", error);
        this.errorMessage = error.response.data.error;
      }
    },
  },
};
</script>

<style>
.container{
  width: 60%;
}

.container-fluid {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
}

.btn {
  max-width: 50%;
}

.delete_btn {
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 5px;
  background-color: rgb(240, 240, 240);
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete_btn:hover {
  background-color: rgb(188, 188, 188);
}

.error-message {
  color: red;
  margin-top: 10px;
  text-align: center;
}
</style>
