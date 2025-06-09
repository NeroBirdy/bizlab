<template>
  <main class="main">
    <slot></slot>
  </main>
  <!-- <footer class="footer relative mt-20">
    <div class="container flex justify-between">
      <div class="left-fot">
        <img class="logo" src="/assets/images/logo-white.png" />
        <p>
          © ЧУДО "Образовательный центр BIZLAB" Лицензия №3256 от 4 марта 2019
          года
        </p>
        <p>
          *Соцсети Instagram и Facebook запрещены в РФ. 21.03.2022 компания Meta
          признана в России экстремистской организацией
        </p>
      </div>
      <div class="right-fot">
        <h2>навигация</h2>
        <div class="grid-div">
          <a href="#">Преимущества</a>
          <a href="#">Наши правила</a>
          <a href="#">Направления</a>
          <a href="#">Вакансии</a>
          <a href="#">Стоимость</a>
          <a href="#">Акции</a>
          <a href="#">Политика конфиденциальности</a>
        </div>
        <p>Сделано дизайн-студией «НАЗЫВАЕМся»</p>
      </div>
    </div>
    <img src="/assets/images/bot.png" class="bot" />
  </footer> -->
</template>

<style lang="scss" scooped>
template{
    min-height: 100%;
    display: grid;
    grid-template-rows: 1fr auto;
}

main{
    min-height: 99vh;
}

.footer {
  background-color: #171717;
  padding: 80px;

  .container {
    width: 80%;
  }
}

.left-fot {
  width: 30%;
  p {
    margin-top: 50px;
    color: #525252;
  }
}

.grid-div {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-row-gap: 10px;
  a {
    font-size: 18px;
    color: white;
  }
}

.right-fot {
  width: 30%;
  color: #525252;

  h2 {
    font-family: "Uncage";
    font-size: 24px;
  }

  p {
    margin-top: 50px;
    font-size: 18px;
  }
}

.bot {
  width: 80%;
  position: absolute;
  bottom: 0;
  left: 10%;
  right: 10%;
}
</style>
