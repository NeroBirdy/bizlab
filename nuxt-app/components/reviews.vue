<template>
  <div class="reviewContent">
    <h1 class="text-center">ОТЗЫВЫ НАШИХ клиентов</h1>
    <div class="grid-container">
      <div class="cards">
        <Review
          v-for="comment in comments"
          color="#F0AC02"
          :name="comment.sender"
          :review="comment.text"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

const comments = ref();

const getComments = async () => {
  const response = await axios.get(`${apiBase}/api/getFeedback`);

  comments.value = response.data;
  console.log(comments);
};

onMounted(() => {
  getComments();
});
</script>

<style lang="scss" scoped>
.reviewContent {
  width: 100vw;
  height: 100vh;
}

.cards {
  display: grid;
  margin-top: 3.5vw;
  width: 90vw;
  grid-template-columns: repeat(auto-fit, minmax(370px, 1fr));
  align-items: center;
  gap: 3vw;
}

.grid-container {
  width: 100vw;
  display: flex;
  justify-content: center;
}

.line {
  position: absolute;
  z-index: 2;
  bottom: -130px;
}

@media (max-width: 1320px) {
  .cards div:nth-child(3) {
    grid-column: 1 / span 2;
    grid-row: 2 / 3;
  }
}

@media (max-width: 767px) {
  .cards {
    div:nth-child(3) {
      grid-column: 1 / 1;
      grid-row: 2 / 3;
    }
  }
}

@media (max-width: 425px) {
  .cards {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}
</style>
