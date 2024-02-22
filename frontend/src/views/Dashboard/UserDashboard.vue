<template>
  <div>
    <UserNavbar />
    <router-view></router-view>
  </div>
</template>

<script>
import UserNavbar from "../../components/UserNavbar/UserNavbar.vue";
export default {
  name: "UserDashboard",
  components: {
    UserNavbar,
  },
};
</script>


<style>
</style>