<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#"
          >Librarian Dashboard</a
        >
        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </div>
    </nav>
</template>

<script>
export default {
  name: "LibrarianNavbar",
    methods:{
        logout(){
            localStorage.removeItem('accessToken');
            this.$router.push('/librarianlogin');
        }
    }
};
</script>

<style>
</style>