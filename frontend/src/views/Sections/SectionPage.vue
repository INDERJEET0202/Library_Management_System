<template>
  <div>
    <LibrarianNavbarVue />
    <!-- <h1>Sections {{ id }}, {{ name }}</h1> -->
    <div class="add-sections">
      <div class="card text-center mt-4">
        <div class="card-body">
          <h5 class="card-title">Add Books to {{name}} section</h5>
          <hr />
          <p class="card-text">
            Add books to view the books in the library.
          </p>
          <button
            type="button"
            class="btn btn-success"
            data-bs-toggle="modal"
            data-bs-target="#staticBackdrop"
          >
            Add
          </button>
          <AddBookModal :sectionName="name"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import LibrarianNavbarVue from "../../components/LibrarianNavbar/LibrarianNavbar.vue";
import AddBookModal from '../../components/Modals/AddBookModal.vue';
export default {
  name: "SectionPage",
  props: ["id", "name"],
  components: {
    LibrarianNavbarVue,
    AddBookModal,
  },

  mounted() {
    // console.log(this.name)
  },
};
</script>

<style>
.add-sections {
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>