<template>
  <div class="content">
    <img
      src="/assets/images/welcomePage/background.png"
      alt="back"
      class="background"
    />
    <div style="display: none">Лучшее место для развития вашего ребенка</div>
    <!-- <a class="parallelogram" href="#"
      ><img src="/assets/images/welcomePage/link.svg" alt="link"
    /></a> -->
  </div>
</template>

<style lang="scss" scooped>
.content {
  @apply w-full relative;
  height: 100vh;
}

.background {
  position: absolute;
  width: 100%;
  height: 100vh;
}

.bizLogo {
  position: absolute;
  bottom: -50px;
  display: none;
}

.vector {
  position: absolute;
  top: -30px;
  display: none;
}

.parallelogram {
  position: absolute;
  width: 487px;
  height: 168px;
  bottom: 260px;
  right: 400px;
  transition: all 0.2s;
  &:hover {
    transform: scaleX(1.1);
  }
}
</style>
