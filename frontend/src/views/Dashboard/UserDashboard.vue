<template>
  <div>
    <UserNavbar />
    <div class="container mt-4">
      <div class="user-info">
        <h3>Welcome, {{ userName }}</h3>
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


<style>
</style>