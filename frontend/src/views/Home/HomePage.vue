<template>
  <div>
    <Navbar />
    <div class="container">
      <h1>Home Page</h1>
      <p>Welcome to the home page of the Bookstore</p>
      <div class="navigation"></div>
    </div>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
export default {
  name: "HomePage",
  components: {
    Navbar,
  },
};
</script>

<style scoped>
.container {
  text-align: center;
  margin-top: 20px;
}
</style>