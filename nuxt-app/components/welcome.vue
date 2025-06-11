<template>
  <div class="content" id="welcome">
    <div class="main-container">
      <div class="main-container-text">
        <div class="line1">Лучшее</div>
        <div class="line2">место для</div>
        <div class="line3">развития</div>
        <div class="line4">вашего ребенка</div>
      </div>
      <div class="main-container-img">
        <img
          src="/assets/images/welcomePage/background.svg"
          alt="back"
          class="background"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scooped>
.content {
  height: 90vh;
  overflow: hidden;
  width: 100vw;
}

.main-container {
  height: 85vh;
  display: flex;
  flex-direction: column;
  margin-top: 5vh;
  max-width: 100vw;
}

.main-container-text {
  display: none;
  width: 100%;
  height: 10%;
  text-align: left;
  font-size: 5vw;
  font-family: 'UnboundedRegular';
  padding-left: 5vw;
  z-index: 2;
  line-height: 12vw;
}

.main-container-img {
  width: 100%;
  height: 90%;
  display: flex;
  align-items: center;
}

.background {
  position: absolute;
  width: 93vw;
  margin-right: 7vw;
  // height: 100vh;
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

.line1, .line2, .line3, .line4 {
  font-family: "Uncage";
}

.line2, .line3 {
  position: relative;
  left: 8vw;
}

.line1 {
  color: rgb(226, 93, 53);
  font-size: 15vw;
}

.line2 {
  font-size: 8vw;
}

.line3 {
  color: rgb(240, 172, 2);
  font-size: 12vw;
}

.line4 {
  font-size: 6vw;
  line-height: 8vw;
}

@media (max-width: 426px) {
  .main-container-text {
    display: block;
  }
  .background {
    content:  url("/assets/images/welcomePage/back_withoutwork.svg");
    width: 100vw;
    margin-right: 0;
    position: relative;
    left: 23vw;
    scale: 1.8;
  }
  header {
    margin-left: 5vw;
    margin-right: 5vw;
  }
}
</style>




