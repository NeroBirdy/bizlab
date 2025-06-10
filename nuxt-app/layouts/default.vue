<template>
  <slot></slot>
  <footer class="footer relative mt-20">
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
  </footer>
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
  padding: 5.5vw;

  .container {
    width: 90%;
  }
}

.left-fot {
  width: 30%;
  p {
    margin-top: 2.5vw;
    color: #525252;
  }
}

.grid-div {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  a {
    font-size: 1.25vw;
    color: rgba(227, 227, 227, 0.7);
  }
}

.grid-div a:nth-child(7) {
  grid-column: 1 / span 2;
  grid-row: 7 / 8;
}

.right-fot {
  max-width: 45%;
  color: #525252;

  h2 {
    font-family: "Uncage";
    font-size: 2vw;
  }

  p {
    margin-top: 50px;
    font-size: 1.25vw;
  }
}

.bot {
  width: 80%;
  position: absolute;
  bottom: 0;
  left: 10%;
  right: 10%;
}

@media (max-width: 768px) {
  .right-fot {
    h2 {
      font-size: 3vw;
    }
    p {
      font-size: 1.7vw;
    }
  }
  .grid-div {
    a {
      font-size: 2vw;
    }
  }
  .left-fot {
    p {
      font-size: 1.7vw;
    }
  }
}

@media (max-width: 425px) {
  .right-fot {
    h2 {
      font-size: 4vw;
    }
    p {
      font-size: 2.5vw;
    }
  }
  .grid-div {
    a {
      font-size: 2.3vw;
    }
  }
  .left-fot {
    p {
      font-size: 2.3vw;
    }
  }
}

@media (min-width: 1441px) {
  .left-fot {
    p {
      font-size: 1.25vw;
    }
  }
}
</style>
