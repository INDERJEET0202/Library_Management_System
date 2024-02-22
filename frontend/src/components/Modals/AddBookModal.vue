<template>
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
            <button type="button" class="btn btn-primary" @click="addBook">
              Add Book
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DOMPurify from "dompurify";
import axios from "axios";
export default {
  name: "AddBookModal",
  data() {
    return {
      newBook: {
        title: "",
        authorName: "",
        content: "",
        section: "",
      },
    };
  },
  mounted() {
    this.setSectionName();
  },
  props: ["sectionName"],
  methods: {
    addBook() {
      console.log(this.newBook);
      this.newBook.title = DOMPurify.sanitize(this.newBook.title);
      this.newBook.authorName = DOMPurify.sanitize(this.newBook.authorName);
      this.newBook.content = DOMPurify.sanitize(this.newBook.content);
      this.newBook.section = DOMPurify.sanitize(this.newBook.section);
      axios
        .post("http://127.0.0.1:5000/api/add/book", this.newBook, {
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
    setSectionName() {
      this.newBook.section = this.sectionName;
    },
  },
};
</script>

<style scoped>
.modal-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>