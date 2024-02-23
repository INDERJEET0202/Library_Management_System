<template>
  <div>
    <LibrarianNavbar />
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <div class="card">
            <div class="card-header">
              <h4>Requested Books</h4>
            </div>
            <div class="card-body">
              <div v-if="requestedBooks.length > 0">
                <table class="table table-bordered">
                  <thead>
                    <tr>
                      <th>Book Name</th>
                      <th>Requested By</th>
                      <th>Give</th>
                      <th>Revoke</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="book in requestedBooks" :key="book.book_id">
                      <td>{{ book.book_name }}</td>
                      <td>{{ book.user_name }}</td>
                      <td>
                        <button
                          class="btn btn-success"
                          @click="
                            grantBookRequest(
                              book.book_id,
                              book.section_id,
                              book.user_id
                            )
                          "
                        >
                          Grant
                        </button>
                      </td>
                      <td>
                        <button
                          class="btn btn-danger"
                          @click="revokeAccess(book.allocation_id)"
                        >
                          Reject
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else>
                <p>No requested books right now.</p>
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
export default {
  name: "BooksRequested",
  components: {
    LibrarianNavbar,
  },
  data() {
    return {
      requestedBooks: [],
    };
  },
  mounted() {
    this.fetchRequestedBooks();
  },
  methods: {
    async fetchRequestedBooks() {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/books/requested",
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        const data = await response.json();
        if (response.ok) {
          this.requestedBooks = data;
          console.log("Requested books: ", data);
        } else {
          console.error("Failed to fetch requested books: ", data.error);
        }
      } catch (error) {
        console.error("Error fetching requested books: ", error);
      }
    },
    async grantBookRequest(bookId, sectionId, userId) {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/books/allocate",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify({
              book_id: bookId,
              section_id: sectionId,
              user_id: userId,
            }),
          }
        );
        const data = await response.json();
        if (response.ok) {
          console.log("Book request granted successfully: ", data.message);
          this.fetchRequestedBooks();
        } else {
          console.error("Failed to grant book request: ", data.error);
        }
      } catch (error) {
        console.error("Error granting book request: ", error);
      }
    },
    async revokeAccess(allocationId) {
      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/delete/request",
          {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
            body: JSON.stringify({
              allocation_id: allocationId,
            }),
          }
        );


        if (!response.ok) {
          throw new Error("Failed to revoke access");
        }
        else{
          this.fetchRequestedBooks();
        }

        const data = await response.json();
        console.log(data);
      } catch (error) {
        console.error("Error revoking access:", error);
      }
    },
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
</style>
