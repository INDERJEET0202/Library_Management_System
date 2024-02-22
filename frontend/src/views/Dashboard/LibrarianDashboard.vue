<template>
  <div>
    <LibrarianNavbar />
    <div class="add-sections">
      <div class="card text-center mt-4">
        <div class="card-body">
          <h5 class="card-title">Add Sections to View</h5>
          <hr />
          <p class="card-text">
            Add sections to view the books in the library.
          </p>
          <button
            type="button"
            class="btn btn-success"
            data-bs-toggle="modal"
            data-bs-target="#exampleModal"
          >
            Add
          </button>
          <div
            class="modal fade"
            id="exampleModal"
            tabindex="-1"
            aria-labelledby="exampleModalLabel"
            aria-hidden="true"
          >
            <div class="modal-dialog modal-dialog-centered">
              <div class="modal-content">
                <div class="modal-header">
                  <h1 class="modal-title fs-5" id="exampleModalLabel">
                    Add a new section
                  </h1>
                  <button
                    type="button"
                    class="btn-close"
                    data-bs-dismiss="modal"
                    aria-label="Close"
                  ></button>
                </div>
                <div class="modal-body">
                  <form class="form-floating">
                    <input
                      type="email"
                      class="form-control"
                      id="floatingInputValue"
                      placeholder="name@example.com"
                      v-model="newSection.title"
                      required
                    />
                    <label for="floatingInputValue">Section Title</label>
                  </form>
                  <div class="form-floating">
                    <input
                      type="date"
                      class="form-control"
                      id="floatingInputValue"
                      placeholder=""
                      v-model="newSection.date"
                      required
                    />
                    <label for="floatingInputValue">Date</label>
                  </div>
                  <div class="form-floating">
                    <textarea
                      class="form-control"
                      placeholder="Add a description here"
                      id="floatingTextarea"
                      v-model="newSection.description"
                      required
                    ></textarea>
                    <label for="floatingTextarea">Description</label>
                  </div>
                </div>
                <div class="modal-footer">
                  <button
                    type="button"
                    class="btn btn-secondary"
                    data-bs-dismiss="modal"
                  >
                    Close
                  </button>
                  <button
                    type="button"
                    class="btn btn-primary"
                    @click="saveSection"
                  >
                    Save changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="search-section container mt-4">
      <input type="text" v-model="searchQuery" placeholder="Search sections..." class="form-control">
    </div>

    <div class="display-sections">
      <h3>All Sections</h3>
      <div class="section-cards">
        <div
          class="card"
          style="width: 18rem"
          v-for="section in filteredSections"
          :key="section.id"
        >
          <div class="card-body">
            <h5 class="card-title">{{ section.name }}</h5>
            <h6 class="card-subtitle mb-2 text-body-secondary">
              Date created: {{ section.date_created }}
            </h6>
            <p class="card-text">
              {{ section.description }}
            </p>
            <div class="buttons">
              <!-- <button type="button" class="btn btn-primary align-self-start">
                Add Books
              </button> -->
              <button
                type="button"
                class="btn btn-primary modal-dialog-centered"
                data-bs-toggle="modal"
                data-bs-target="#staticBackdrop"
                @click="setSection(section.name)"
              >
                Add Books
              </button>
              <router-link
                :to="
                  '/librarian/dashboard/viewsection/' +
                  section.id +
                  '/' +
                  section.name
                "
                class="btn btn-success align-self-start"
              >
                View Section
              </router-link>
            </div>

            <!-- Modal -->
            <div>
              <div
                class="modal fade"
                id="staticBackdrop"
                data-bs-backdrop="static"
                data-bs-keyboard="false"
                tabindex="-1"
                aria-labelledby="staticBackdropLabel"
                aria-hidden="true"
              >
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="staticBackdropLabel">
                        Add a book
                      </h1>
                      <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <div class="modal-body">
                      <form class="form-floating">
                        <input
                          type="email"
                          class="form-control"
                          id="floatingInputValue"
                          placeholder="name@example.com"
                          v-model="newBook.title"
                          required
                        />
                        <label for="floatingInputValue">Book Title</label>
                      </form>

                      <form class="form-floating">
                        <input
                          type="email"
                          class="form-control"
                          id="floatingInputValue"
                          placeholder="name@example.com"
                          v-model="newBook.authorName"
                          required
                        />
                        <label for="floatingInputValue">Author Name</label>
                      </form>

                      <form class="form-floating">
                        <input
                          type="email"
                          class="form-control"
                          id="floatingInputValue"
                          placeholder="name@example.com"
                          v-model="newBook.content"
                          required
                        />
                        <label for="floatingInputValue">Content</label>
                      </form>

                      <form class="form-floating">
                        <input
                          type="email"
                          class="form-control"
                          id="floatingInputValue"
                          v-model="newBook.section"
                          required
                        />
                        <label for="floatingInputValue">Book Section</label>
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
                      <button
                        type="button"
                        class="btn btn-primary"
                        @click="addBook"
                      >
                        Add Book
                      </button>
                    </div>
                  </div>
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
import LibrarianNavbar from "../../components/LibrarianNavbar/LibrarianNavbar.vue";
import axios from "axios";
import DOMPurify from "dompurify";

export default {
  name: "LibrarianDashboard",
  components: {
    LibrarianNavbar,
  },
  data() {
    return {
      newSection: {
        title: "",
        date: "",
        description: "",
      },
      sections: [],
      newBook: {
        title: "",
        authorName: "",
        content: "",
        section: "",
      },
      searchQuery: "", // Data property to hold search query
    };
  },
  mounted() {
    this.fetchSections();
  },
  computed: {
    // Filter sections based on search query
    filteredSections() {
      return this.sections.filter(section =>
        section.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    saveSection() {
      this.newSection.title = DOMPurify.sanitize(this.newSection.title);
      this.newSection.date = DOMPurify.sanitize(this.newSection.date);
      this.newSection.description = DOMPurify.sanitize(this.newSection.description);
      axios
        .post("http://127.0.0.1:5000/api/add/new-section", this.newSection, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          console.log("Section added successfully.", response.data);
          this.newSection = {
            title: "",
            date: "",
            description: "",
          };
          // reload the page
          location.reload();
          alert(response.data.message);
        })
        .catch((error) => {
          console.error("Error adding section:", error);
        });
    },
    fetchSections() {
      axios
        .get("http://127.0.0.1:5000/api/sections", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          this.sections = response.data;
          console.log(this.sections);
        })
        .catch((error) => {
          console.error("Error fetching sections:", error);
        });
    },
    addBook() {
      console.log(this.newBook);
      this.newBook.title = DOMPurify.sanitize(this.newBook.title);
      this.newBook.authorName = DOMPurify.sanitize(this.newBook.authorName);
      this.newBook.content = DOMPurify.sanitize(this.newBook.content);
      this.newBook.section = DOMPurify.sanitize(this.newBook.section);
      axios.post("http://127.0.0.1:5000/api/add/book", this.newBook, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      })
      .then((response) => {
        alert(response.data.message);
        this.newBook = {
          title: "",
          authorName: "",
          content: "",
          section: "Please select the section to add the book to.",
        };
      })
      .catch((error) => {
        console.error("Error adding book:", error);
      });
    },
    setSection(sectionName) {
      this.newBook.section = sectionName;
    },
  },
};
</script>

<style scoped>
.add-sections {
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.display-sections {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  padding-top: 20px;
}

.section-cards {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
  gap: 20px;
}

.card {
  width: 18rem;
}

.buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.search-section {
  margin-bottom: 20px;
}
</style>
