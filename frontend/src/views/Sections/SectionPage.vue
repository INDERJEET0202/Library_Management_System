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
                        <td>
                          <div class="buttons">
                            <button
                              type="button"
                              class="btn btn-primary"
                              data-bs-toggle="modal"
                              data-bs-target="#staticBackdrop1"
                              @click="editBook(book)"
                            >
                              Edit
                            </button>

                            <button
                              type="button"
                              class="btn delete btn-danger center"
                              @click="deleteBook(book.book_id)"
                            >
                              Delete
                            </button>
                          </div>
                          <!-- Modal -->
                          <div
                            class="modal fade"
                            id="staticBackdrop1"
                            data-bs-backdrop="static"
                            data-bs-keyboard="false"
                            tabindex="-1"
                            aria-labelledby="staticBackdropLabel"
                            aria-hidden="true"
                          >
                            <div class="modal-dialog">
                              <div class="modal-content">
                                <div class="modal-header">
                                  <h1
                                    class="modal-title fs-5"
                                    id="staticBackdropLabel"
                                  >
                                    Modal title
                                  </h1>
                                  <button
                                    type="button"
                                    class="btn-close"
                                    data-bs-dismiss="modal"
                                    aria-label="Close"
                                  ></button>
                                </div>
                                <div class="modal-body">
                                  <form @submit.prevent="updateBook">
                                    <div class="mb-3">
                                      <label
                                        for="editBookName"
                                        class="form-label"
                                        >Book Name</label
                                      >
                                      <input
                                        type="text"
                                        class="form-control"
                                        id="editBookName"
                                        v-model="editBookData.book_name"
                                        required
                                      />
                                    </div>
                                    <div class="mb-3">
                                      <label
                                        for="editBookAuthor"
                                        class="form-label"
                                        >Author</label
                                      >
                                      <input
                                        type="text"
                                        class="form-control"
                                        id="editBookAuthor"
                                        v-model="editBookData.author"
                                        required
                                      />
                                    </div>
                                  </form>
                                </div>
                                <div class="modal-footer">
                                  <button
                                    type="button"
                                    class="btn btn-secondary"
                                    data-bs-dismiss="modal"
                                  >
                                    Close
                                  </button>
                                  <button type="submit" class="btn btn-primary" @click="updateBook()">
                                    Save Changes
                                  </button>
                                </div>
                              </div>
                            </div>
                          </div>
                        </td>
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
      editBookData: {
        book_name: "",
        author: "",
      },
    };
  },
  components: {
    LibrarianNavbarVue,
    AddBookModal,
  },
  methods: {
    editBook(book) {
      this.editBookData = {
        book_id: book.book_id,
        book_name: book.book_name,
        author: book.author,
      };
      console.log(this.editBookData);
    },
    async updateBook() {
      try {
        const response = await axios.put(
          `http://127.0.0.1:5000/api/books/update`,
          this.editBookData,
          {
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          console.log("Book updated: ", response.data);
          alert("Book updated successfully!");
          this.fetchSectionBooks();
        } else {
          console.error("Failed to update book: ", response.data.error);
        }
      } catch (error) {
        console.error("Failed to update book: ", error.message);
      }
    },
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

.buttons {
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 10px;
}
</style>