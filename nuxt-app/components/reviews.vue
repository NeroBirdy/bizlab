<template>
  <div class="relative w-full justify-center flex">
    <div class="ml-auto mr-auto">
      <h1 class="text-center">ОТЗЫВЫ НАШИХ клиентов</h1>
      <div class="cards">
        <Review
          v-for="comment in comments"
          color="#F0AC02"
          :name="comment.sender"
          :review="comment.text"
        />
      </div>
    </div>
    <img
      src="/assets/images/reviewsPage/l-line.svg"
      alt=""
      class="line left-0"
    />
    <img
      src="/assets/images/reviewsPage/r-line.svg"
      alt=""
      class="line right-0"
    />
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
.cards {
  display: flex;
  column-gap: 93px;
  margin-top: 50px;
}

.line {
  position: absolute;
  z-index: 2;
  bottom: -130px;
}
</style>
