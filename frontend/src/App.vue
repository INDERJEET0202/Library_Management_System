<template>
  <div>
    <Navbar v-if="isAppPage" />
    <router-view />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    Navbar,
  },
  computed: {
    isAppPage() {
      // Check if the current route corresponds to the App.vue page
      return this.$route.name === 'App';
    },
  },
};
</script>

<style scoped>
/* Add your scoped styles here */
</style>
