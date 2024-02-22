<template>
  <div>
    <LibrarianNavbarVue />
    <!-- <h1>Sections {{ id }}, {{ name }}</h1> -->
    <div class="add-sections">
      <div class="card text-center mt-4">
        <div class="card-body">
          <h5 class="card-title">Add Books to {{ name }} section</h5>
          <hr />
          <p class="card-text">Add books to view the books in the library.</p>
          <button
            type="button"
            class="btn btn-success"
            data-bs-toggle="modal"
            data-bs-target="#staticBackdrop"
          >
            Add
          </button>
          <AddBookModal :sectionName="name" />
        </div>
      </div>
    </div>
    <div class="container">
      <div class="books mt-4">
        <div class="row">
          <div class="col-md-12">
            <div class="card">
              <div class="card-header">
                <h4>Books</h4>
              </div>
              <div class="card-body">
                <div v-if="books.length > 0">
                  <table class="table table-bordered">
                    <thead>
                      <tr>
                        <th>Book Name</th>
                        <th>Author</th>
                        <th>Function</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="book in books" :key="book.book_id">
                        <td>{{ book.book_name }}</td>
                        <td>{{ book.author }}</td>
                        <button
                          type="button"
                          class="btn delete btn-danger center"
                          @click="deleteBook(book.book_id)"
                        >
                          Delete
                        </button>
                      </tr>
                    </tbody>
                  </table>
                </div>
                <div v-else>
                  <p>No books available.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import LibrarianNavbarVue from "../../components/LibrarianNavbar/LibrarianNavbar.vue";
import AddBookModal from "../../components/Modals/AddBookModal.vue";
export default {
  name: "SectionPage",
  props: ["id", "name"],
  data() {
    return {
      books: [],
    };
  },
  components: {
    LibrarianNavbarVue,
    AddBookModal,
  },
  methods: {
    async fetchSectionBooks() {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/fetch/section/books",
          {
            section_id: this.id,
          },
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );

        if (response.status === 200) {
          console.log("Section Books:", response.data);
          this.books = response.data;
        } else {
          console.error("Failed to fetch section books: ", response.data.error);
        }
      } catch (error) {
        console.error("Failed to fetch section books: ", error.message);
      }
    },
    async deleteBook(book_id) {
      try {
        const response = await axios.delete(
          `http://127.0.0.1:5000/api/books/delete`,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            data: { book_id: book_id },
          }
        );
        console.log(response.data);
        this.fetchSectionBooks();
      } catch (error) {
        console.error("Failed to delete book: ", error.message);
      }
    },
  },
  mounted() {
    // console.log(this.name)
    this.fetchSectionBooks();
  },
};
</script>

<style scoped>
.add-sections {
  display: flex;
  justify-content: center;
  align-items: center;
}

.delete {
  margin: 10px 10px;
  color: white;
  background-color: #f13535;
}

.delete:hover {
  background-color: #aa0000;
}
</style>