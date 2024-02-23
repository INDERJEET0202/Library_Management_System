<template>
    <div class="container">
      <div class="div1">
        <h3 style="text-align: center" class="mb-3">
          Stats of book issued on each section
        </h3>
        <canvas ref="pieChart" height="400" width="400" class="canvas"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import Chart from "chart.js/auto";
  import axios from "axios";
  
  export default {
    name: "AllStats",
    mounted() {
      this.getStatistics();
    },
    data() {
      return {
        bookIssuedCount: null,
      };
    },
    methods: {
      renderPieChart() {
        if (!this.bookIssuedCount || !this.bookIssuedCount.allocated_sections) {
          return;
        }
  
        const ctx = this.$refs.pieChart.getContext("2d");
        const labels = this.bookIssuedCount.allocated_sections.map(section => section.section_name);
        const data = this.bookIssuedCount.allocated_sections.map(section => section.books_count);
  
        new Chart(ctx, {
          type: "doughnut",
          data: {
            labels: labels,
            datasets: [
              {
                label: "Books Read",
                data: data,
                backgroundColor: [
                  "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(255, 206, 86, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(255, 159, 64, 0.2)",
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(255, 206, 86, 1)",
                  "rgba(75, 192, 192, 1)",
                  "rgba(153, 102, 255, 1)",
                  "rgba(255, 159, 64, 1)",
                ],
                borderWidth: 1,
              },
            ],
          },
          options: {
            title:{
              display: true,
              text: 'Books Issued by Section',
              fontSize: 20,
              color: 'black'
            },
            responsive: false,
            maintainAspectRatio: true,
          },
        });
      },
      async getStatistics() {
        try {
          const response = await axios.get(
            "http://127.0.0.1:5000/api/books/allocated-by-user",
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
              },
            }
          );
          console.log(response.data);
          this.bookIssuedCount = response.data;
          this.renderPieChart();
        } catch (error) {
          console.error("Failed to get statistics: ", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .div1{
    margin-top: 20px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  </style>
  