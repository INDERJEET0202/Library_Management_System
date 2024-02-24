<template>
  <div>
    <div class="all-books">
      <h3>All Books</h3>
      <div v-for="book in books" :key="book.id" class="content">
        <div class="book-details">
          <p><strong>Title: </strong> {{ book.name }}</p>
          <p><strong>Author:</strong> {{ book.authors }}</p>
          <p><strong>Section:</strong> {{ book.section }}</p>
        </div>
        <div class="button">
          <button
            v-if="book.allocated === 1 && book.read === 1"
            type="button"
            class="btn btn-completed"
          >
            Completed
          </button>
          <button
            v-else-if="book.allocated === 1 && book.read === 0"
            type="button"
            class="btn btn-warning"
          >
            Already Allocated
          </button>
          <button
            v-else-if="book.requested === 1"
            type="button"
            class="btn btn-warning"
          >
            Already Requested
          </button>
          <!-- <button
            v-else-if="book.requested === 1 && book.read === 1 "
            type="button"
            class="btn btn-warning"
          >
            Already Requested
          </button> -->
          <button
            v-else-if="book.allocated === 0 && book.read === 0"
            type="button"
            class="btn btn-primary"
            @click="handleRequest(book.id, book.section)"
          >
            Request
          </button>
          <button
            v-else-if="book.read === 1"
            type="button"
            class="btn btn-completed"
          >
            Completed
          </button>
          <button
            v-if="book.read === 1"
            type="button"
            class="btn btn-request_again"
            @click="handleRequest(book.id, book.section)"
          >
            Request Again
          </button>
        </div>
      </div>
    </div>
  </div>
</template>




<script>
import axios from "axios";
export default {
  name: "AllBooks",
  data() {
    return {
      books: [],
    };
  },
  created() {
    this.fetchBooks();
  },
  methods: {
    fetchBooks() {
      axios
        .get("http://127.0.0.1:5000/api/books", {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          this.books = response.data;
          console.log(this.books);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    handleRequest(bookId, sectionName) {
      console.log(bookId, sectionName);
      const requestData = {
        book_id: bookId,
        section_name: sectionName,
      };
      axios
        .post("http://127.0.0.1:5000/api/request/book", requestData, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          },
        })
        .then((response) => {
          console.log(response.data);
          console.log("Request sent");
          this.fetchBooks();
        })
        .catch((error) => {
          alert(error.response.data.error)
          console.log(error);
        });
    },
  },
};
</script>

<style scoped>
.all-books {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2rem;
  font-family: Poppins, sans-serif;
}

.content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 70%;
  background-color: #f6f6f6;
  border-radius: 10px;
  padding: 1rem;
  margin-top: 1rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.book-details {
  display: flex;
  align-items: center;
  text-align: center;
  justify-content: space-between;
  flex-direction: row;
  gap: 2rem;
}

.btn {
  max-width: 100%;
  background-color: rgba(72, 255, 72, 0.719);
  color: black;
  border: none;
}

.btn:hover {
  background-color: rgba(72, 255, 72, 0.9);
}

.btn-warning {
  background-color: rgba(255, 221, 0, 0.719);
  color: black;
  pointer-events: none; 
  cursor: not-allowed;
  opacity: 0.5;
}

.btn-warning:hover {
  background-color: rgba(255, 221, 0, 0.9);
}

.btn-completed{
  background-color: rgba(0, 255, 0, 0.719);
  color: black;
  pointer-events: none; 
  cursor: not-allowed;
  opacity: 0.5;
}

.request_again{
  background-color: rgba(0, 255, 0, 0.719);
  color: black;
  pointer-events: none; 
  cursor: not-allowed;
  opacity: 0.5;
  margin-right: 5px;
}

.button{
  display: flex;
  gap: 10px;
}
</style>