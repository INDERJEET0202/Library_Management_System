<template>
  <div>
    <UserNavbar />
    <div class="container mt-4">
      <div class="user-info mb-4">
        <h3>Welcome, {{ userName }}</h3>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import UserNavbar from "../../components/UserNavbar/UserNavbar.vue";
import axios from "axios";
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
  methods: {
    async setUsersLastVisitTime(){
      const response = await axios.post("http://127.0.0.1:5000/api/track-last-login" ,{}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        }
      })
      if (response.status === 200) {
        console.log("Last login time updated: ", response.data);
      } else {
        console.error("Failed to update last login time: ", response.data.error);
      }
    }
  },
  mounted() {
    this.userName = JSON.parse(localStorage.getItem("user"));
    this.setUsersLastVisitTime();
  },
};
</script>


<style scoped>
.user-info {
  text-align: center;
  margin-top: 20px;
}
</style>