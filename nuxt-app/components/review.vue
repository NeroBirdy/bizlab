<script setup>
const props = defineProps({
  color: String,
  name: String,
  review: String,
});
</script>

<template>
  <div class="review-card">
    <img src="/assets/images/reviewsPage/отзыв.svg" class="jaba"/>
    <div class="block">
      <h2 class="">{{ name }}</h2>
      <p class="">{{ review }}</p>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.review-card {
  position: relative;
  display: flex;
  justify-content: center;
  img {
    position: relative;
    z-index: 2;
    width: 370px;
  }
}

.block {
  width: 370px;
  height: 212px;
  padding: 1.5vw;
  position: absolute;
  border-radius: 40px;
  z-index: 3;
  top: 37%;
  background-color: rgba(222, 116, 10, 0);

  h2,
  p {
    color: white;
  }

  h2 {
    margin-top: 2vw;
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

@media (min-width: 1441px) {
  .block{
    h2 {
      margin-top: 1vw;
      line-height: 1.4vw;
    }
  }
}

@media (max-width: 1024px) {
  .review-card img {
    width: 300px;
    height: 273px;
  }

  .block {
    width: 300px;
    height: 170px;
    h2 {
      font-size: 18px;
    }
    p {
      font-size: 14px;
    }
  }
}

@media (max-width: 767px) {
  .block {
    padding: 2.5vw;
  }
}

@media (max-width: 425px) {
  .review-card {
    img {
    width: 250px;
    height: 228px;
    }
  }

  .block {
    width: 250px;
    height: 142px;
    border-radius: 32px;
    padding: 3vw;
    h2 {
      font-size: 13px;
    }
    p {
      font-size: 10px;
    }
  }
}

@media (min-width: 1800px) {
  .review-card img {
    width: 500px;
    height: 455px;
  }

  .block {
    width: 500px;
    height: 290px;
    border-radius: 46px;
    h2 {
      font-size: 32px;
      line-height: 2vw;
      margin-bottom: 1.8vw;
    }
    p {
      font-size: 24px;
      line-height: 1.5vw;
    }
  }
}

@media (min-width: 2000px) {
  .block {
    h2 {
      font-size: 32px;
      line-height: 1.5vw;
      margin-bottom: 1vw;
      margin-top: 0.8vw;
    }
    p {
      font-size: 24px;
      line-height: 1.5vw;
    }
  }
}
</style>
