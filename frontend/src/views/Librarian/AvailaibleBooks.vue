<template>
  <div>
    <LibrarianNavbar />
    <div class="container">
        <div class="all-books mt-4">
            <h3>Available Books</h3>
            <!-- Search box -->
            <div class="search-section">
                <input type="text" v-model="searchQuery" placeholder="Search books..." class="form-control">
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-body">
                            <div v-if="filteredBooks.length > 0">
                                <table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th>Book Name</th>
                                            <th>Author</th>
                                            <th>Section</th>
                                            <th>Availability</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="book in filteredBooks" :key="book.book_id">
                                            <td>{{ book.book_name }}</td>
                                            <td>{{ book.authors }}</td>
                                            <td>{{ book.section_name }}</td>
                                            <td>{{ book.status }}</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div v-else>
                                <p>No books available right now.</p>
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
import LibrarianNavbar from "../../components/LibrarianNavbar/LibrarianNavbar.vue";
import { host } from "../../utils/APIRoutes.js";
export default {
  name: "AvailableBooks",
  components: {
    LibrarianNavbar,
  },
  data() {
    return {
      books: [],
      searchQuery: '', // Data property to hold search query
    };
  },
  methods: {
    async fetchAllBooks() {
      try {
        console.log(process.env.NODE_ENV)
        console.log(host)
        const response = await axios.get(
          `${host}/api/fetch/librarian/books`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            },
          }
        );
        this.books = response.data;
        console.log(this.books);
      } catch (error) {
        console.log(error);
      }
    },
  },
  computed: {
    filteredBooks() {
      return this.books.filter(book =>
        book.book_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.authors.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.section_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
        book.status.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
    created() {
        this.fetchAllBooks();
    },
};
</script>

<style>
.search-section {
  margin-bottom: 20px;
}
</style>
