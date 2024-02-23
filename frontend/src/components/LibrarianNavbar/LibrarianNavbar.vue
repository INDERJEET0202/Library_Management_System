<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <div class="elements">
          <router-link to="/librarian/dashboard" class="nav-link">Librarian Dashboard</router-link>
          <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/librarian/dashboard/requestedbooks" class="nav-link">Requested Books</router-link>
        <router-link to="/librarian/dashboard/allocatedbooks" class="nav-link">Allocated Books</router-link>
        <router-link to="/librarian/dashboard/availaiblebooks" class="nav-link">Availaible Books</router-link>
        <router-link to="/librarian/dashboard/stats" class="nav-link">Stats</router-link>
        </div>
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
            localStorage.removeItem('userType');
            this.$router.push('/librarianlogin');
        }
    }
};
</script>

<style scoped>
.elements{
    display: flex;
    justify-content: space-between;
    gap: 30px;
}
</style>