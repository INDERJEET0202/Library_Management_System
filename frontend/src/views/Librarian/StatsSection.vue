<template>
  <div>
    <LibrarianNavbar />
    <div class="container">
      <h2 class="text-center mt-4">Overall Stats</h2>
      <div class="statistics mt-4">
        <div class="div1">
          <h3 style="text-align: center" class="mb-3">
            Stats of book issued each day
          </h3>
          <canvas
            ref="barChart"
            height="400"
            width="400"
            class="canvas"
          ></canvas>
        </div>
        <div class="div2">
          <h3 style="text-align: center" class="mb-3">
            Stats of books per section
          </h3>
          <canvas
            ref="pieChart"
            height="400"
            width="400"
            class="canvas"
          ></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import LibrarianNavbar from "@/components/LibrarianNavbar/LibrarianNavbar.vue";
import axios from "axios";

export default {
  name: "StatsSection",
  components: {
    LibrarianNavbar,
  },
  data() {
    return {
      bookIssuedCount: [],
      booksPerSectionCount: [],
    };
  },
  mounted() {
    this.getBookCount();
    this.getBooksPerSection();
  },
  methods: {
    renderLineChart() {
      const ctx = this.$refs.barChart.getContext("2d");

      const labels = this.bookIssuedCount.map((entry) => entry.date_of_issue);
      const issuedCounts = this.bookIssuedCount.map(
        (entry) => entry.issued_count
      );

      new Chart(ctx, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Books Issued Count",
              data: issuedCounts,
              fill: false,
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
              backgroundColor: "rgba(75, 192, 192, 0.2)",
            },
          ],
        },
        options: {
          responsive: false,
          maintainAspectRatio: true,
        },
      });
    },
    renderPieChart() {
      const ctx = this.$refs.pieChart.getContext("2d");

      const labels = this.booksPerSectionCount.map(
        (entry) => entry.section_name
      );
      const bookCounts = this.booksPerSectionCount.map(
        (entry) => entry.books_count
      );

      new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Books Per Section",
              data: bookCounts,
              fill: false,
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
              backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
                "rgba(255, 159, 64, 0.2)",
              ],
            },
          ],
        },
        options: {
          title: {
            display: true,
            text: "World Wide Wine Production 2018",
          },
          responsive: false,
          maintainAspectRatio: true,
        },
      });
    },

    async getBookCount() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/books/issued-count"
        );
        console.log(response.data);
        this.bookIssuedCount = response.data;
        this.renderLineChart();
      } catch (error) {
        console.error("Error fetching book count:", error);
      }
    },
    async getBooksPerSection() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/api/books-per-section"
        );
        console.log(response.data);
        this.booksPerSectionCount = response.data;
        this.renderPieChart();
      } catch (error) {
        console.error("Error fetching books per section:", error);
      }
    },
  },
  // props: {
  //   bookIssuedCount: {
  //     type: Array,
  //     required: true,
  //   },
  // },
};
</script>

<style scoped>
.statistics {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 3rem;
}
</style>