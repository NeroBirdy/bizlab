<script setup>
const props = defineProps({
  color: String,
  name: String,
  review: String,
});
</script>

<template>
  <div class="review-card">
    <img src="/assets/images/reviewsPage/jaba.png" class="jaba" />
    <div class="block" :style="{ backgroundColor: color }">
      <h2 class="">{{ name }}</h2>
      <p class="">{{ review }}</p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.review-card {
  position: relative;
  img {
    position: relative;
    z-index: 2;
  }
}

.block {
  width: 475px;
  height: 275px;
  position: absolute;
  border-radius: 50px;
  z-index: 1;
  top: 160px;

  h2,
  p {
    margin-left: 13%;
    margin-right: 13%;
    color: white;
  }

  h2 {
    margin-top: 30px;
    margin-bottom: 10px;
    font-family: "UnboundedSemiBold";
    font-size: 24px;
  }

  p {
    font-family: "UnboundedRegular";
    font-size: 17px;
    line-height: 22px;
  }
}
</style>
