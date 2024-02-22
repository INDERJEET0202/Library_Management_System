<template>
  <div class="container">
    <div class="row">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header">
            <h4>Current</h4>
          </div>
          <div class="card-body">
            <div v-if="myBooks.length > 0">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Book Name</th>
                    <th>Author</th>
                    <th>Section</th>
                    <th>Function</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="book in myBooks" :key="book.book_id">
                    <td>{{ book.book_title }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.section }}</td>
                    <td class="ano">
                      <button
                        type="button"
                        class="btn"
                        style="background-color: rgb(12, 183, 0);"
                        @click="
                          readBook(book.content)
                        "
                      >
                        Read
                      </button>
                      <button
                        type="button"
                        class="btn btn-warning"
                        
                        @click="
                          returnBook(
                            book.allocation_id,
                            book.book_id,
                            book.userId
                          )
                        "
                      >
                        Return
                      </button>
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
    <div class="row mt-4">
      <div class="col-md-12">
        <div class="card">
          <div class="card-header">
            <h4>Completed</h4>
          </div>
          <div class="card-body">
            <div v-if="returnedBooks.length > 0">
              <table class="table table-bordered">
                <thead>
                  <tr>
                    <th>Book Name</th>
                    <th>Author</th>
                    <th>Section</th>
                    <th>Function</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="book in returnedBooks" :key="book.book_id">
                    <td>{{ book.book_title }}</td>
                    <td>{{ book.author }}</td>
                    <td>{{ book.section }}</td>
                    <td>
                      <button
                        type="button"
                        class="btn btn-primary"
                        data-bs-toggle="modal"
                        data-bs-target="#staticBackdrop"
                      >
                        Feedback
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>

              <!-- Modal -->
              <div
                class="modal fade"
                id="staticBackdrop"
                data-bs-backdrop="static"
                data-bs-keyboard="false"
                tabindex="-1"
                aria-labelledby="staticBackdropLabel"
                aria-hidden="true"
              >
                <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="staticBackdropLabel">
                        Please leave a feedback
                      </h1>
                      <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                      ></button>
                    </div>
                    <div class="modal-body">
                      <form>
                        <div class="mb-3">
                          <label for="recipient-name" class="col-form-label"
                            >Rating (from 1-5 in numbers):</label
                          >
                          <input
                            type="text"
                            class="form-control"
                            id="recipient-name"
                            v-model="rating"
                          />
                        </div>
                        <div class="mb-3">
                          <label for="message-text" class="col-form-label"
                            >Comments:</label
                          >
                          <textarea
                            class="form-control"
                            id="message-text"
                            v-model="comments"
                          ></textarea>
                        </div>
                      </form>
                    </div>
                    <div class="modal-footer">
                      <button
                        type="button"
                        class="btn"
                        style="background-color: rgb(213, 0, 0);"
                        data-bs-dismiss="modal"
                      >
                        Close
                      </button>
                      <button
                        type="button"
                        class="btn"
                        style="background-color: rgb(12, 183, 0);"
                        @click="handleSubmitFeedback()"
                      >
                        Submit
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else>
              <p>No books available.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "MyBooks",
  data() {
    return {
      myBooks: [],
      returnedBooks: [],
      rating: null,
      comments: "",
    };
  },
  methods: {
    async fetchMyBooks() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/fetch_my_books",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          console.log("My Books:", response.data);
          this.myBooks = response.data;
        } else {
          console.error("Failed to fetch my books");
        }
      } catch (error) {
        console.error("Error fetching my books:", error);
      }
    },
    async returnBook(allocation_id, book_id, user_id) {
      try {
        const response = await axios.post(
          "http://127.0.0.1:5000/api/return/book",
          {
            allocation_id: allocation_id,
            book_id: book_id,
            user_id: user_id,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          console.log("Book returned successfully");
          this.fetchMyBooks();
        } else {
          console.error("Failed to return the book");
        }
      } catch (error) {
        console.error("Error returning the book:", error);
      }
    },
    async fetchReturnedBooks() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/fetch_returned_books",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        if (response.status === 200) {
          this.returnedBooks = response.data;
        } else {
          console.error("Failed to fetch returned books");
        }
      } catch (error) {
        console.error("Error fetching returned books:", error);
      }
    },
    async readBook(content) {
      console.log(content);
      const linkUrl = content;
      window.open(linkUrl, "_blank");
    },
    async handleSubmitFeedback() {
      console.log(this.rating, this.comments);
      alert("Feedback submitted successfully \nThank you!");
    },
  },
  mounted() {
    this.fetchMyBooks();
    this.fetchReturnedBooks();
  },
};
</script>


<style scoped>
.btn {
  display: flex;
  justify-content: center;
  background-color: coral;
  color: white;
  border: none;
  margin-left: 10px;
  margin-top: 5px;
  margin-bottom: 5px;
  padding: 5px 10px;
}

.btn:hover {
  background-color: #ff4500;
}

.ano{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
}
</style>