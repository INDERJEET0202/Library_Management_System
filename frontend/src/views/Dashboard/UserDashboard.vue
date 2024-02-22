<template>
  <div>
    <UserNavbar />
    <div class="container mt-4">
      <div class="user-info mb-4">
        <h3>Welcome, {{ userName }}</h3>
        <br>
        Please Navigate to <strong>My Books</strong> section to see your books
        <hr>
        <span class="">Please navigate to <strong>All Books</strong> section to see all the books</span>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import UserNavbar from "../../components/UserNavbar/UserNavbar.vue";
export default {
  data() {
    return {
      userName: "",
    };
  },
  name: "UserDashboard",
  components: {
    UserNavbar,
  },
  mounted() {
    this.userName = JSON.parse(localStorage.getItem("user"));
  },
};
</script>


<style scoped>
.user-info {
  text-align: center;
  margin-top: 20px;
}
</style>