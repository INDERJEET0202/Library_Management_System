<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <router-link to="/user/dashboard" class="nav-link" activeClassName="active">User Dashboard</router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link to="/" class="nav-link" activeClassName="active">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/dashboard/my-books" class="nav-link" activeClassName="active">My Books</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/dashboard/all-books" class="nav-link" activeClassName="active">All Books</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/dashboard/all-stats" class="nav-link" activeClassName="active">Stats</router-link>
            </li>
          </ul>
          <form class="d-flex" role="search">
            <input
              class="form-control me-2"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            <button class="btn btn-outline-success" type="submit">
              Filter
            </button>
          </form>
          <button class="btn btn-outline-danger" style="margin-left: 10px" @click="logout">Logout</button>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: "UserNavbar",
  methods:{
    logout(){
        localStorage.removeItem('accessToken');
        localStorage.removeItem('user');
        this.$router.push('/userlogin');
    }
  }
};
</script>

<style>
</style>