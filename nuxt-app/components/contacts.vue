<template>
  <div class="container">
    <h1 class="flex gap-10 justify-center mb-20">
      <span class="highlight">Контакты </span> центра
    </h1>
    <div class="flex main-block justify-between">
      <div class="flex contact-card">
        <img src="/assets/images/welcomePage/jababa.png" />
        <div class="contact-container">
          <h2>Находимся по адресу:</h2>
          <p>г. Ханты-Мансийск,</p>
          <p>ул. Свердлова д. 28</p>
        </div>
      </div>
      <div class="mr-auto ml-auto">
        <img src="/assets/images/welcomePage/zigzak.png" class="half-point" />
      </div>
      <div class="right flex contact-card">
        <div class="contact-container">
          <h2>Электронная почта:</h2>
          <p>perezagruxkahm@mail.ru</p>
          <h2>Наш телефон:</h2>
          <p>+7 952 702 50 50</p>
        </div>
        <img src="/assets/images/welcomePage/jababa.png" />
      </div>
    </div>
    <div class="flex contact-card justify-center mt-20">
      <div class="contact-container vk-block justify-center">
        <h2>Можете следить за нашими нововостями в группе ВКонтакте</h2>
        <div class="flex justify-between">
          <img src="/assets/images/links/vk.svg" />
          <p>Образовательная лаборатория “BizLab”</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
.highlight {
  color: red;
}

.container {
  width: 80%;
}

.contact-container {
  display: flex;
  flex-direction: column;
  gap: 15px;
  background-color: #f0ac02;
  width: 400px;
  border-radius: 50px;
  height: 225px;
  padding: 25px;

  h2 {
    color: white;
    font-family: "UnboundedSemiBold";
    font-size: 24px;
  }

  p {
    font-family: "UnboundedRegular";
    font-size: 17px;
    line-height: 22px;
    color: white;
  }
}

.contact-card {
  align-items: end;
  img {
    position: relative;
    right: -20px;
    height: 70%;
  }
}

.right {
  margin-right: 0;
  img {
    position: relative;
    transform: scale(-1, 1);
    right: 0;
    left: -50px;
  }
}

.half-point {
  justify-content: center;
  position: relative;
  top: -60px;
  height: 150%;
}

.main-block {
  height: 200px;
}

.vk-block {
  width: 500px;
  h2 {
    text-align: center;
    font-size: 20px;
  }

  img {
    display: block;
    width: 100px;
    height: 70px;
    display: flex;
  }

  p {
    display: flex;
    width: 70%;
    height: 70px;
    align-items: center;
  }
}
</style>
