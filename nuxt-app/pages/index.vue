<template>
  <header>
    <div class="flex w-full h-full justify-between items-center relative">
      <img class="logo" src="/assets/images/bizlap-logo.svg" alt="bizlab" />
      <nav class="navigate">
        <a href="#">О нас</a>
        <a href="#">Курсы</a>
        <a href="#">Команда</a>
        <a href="#">Отзывы</a>
        <a href="#">Записаться</a>
        <a href="#">Контакты</a>
      </nav>
      <div class="social-links">
        <a href="tel:+79995554443"
          ><img src="/assets/images/links/number.svg" alt="Номер телефона"
        /></a>
        <a href="#"
          ><img src="/assets/images/links/whatsApp.svg" alt="WhatsApp"
        /></a>
        <a href="#"><img src="/assets/images/links/vk.svg" alt="VK" /></a>
        <a href="#"
          ><img src="/assets/images/links/instagram.svg" alt="Instagram"
        /></a>
      </div>
    </div>
  </header>
  <main class="mainStyle">
    <Welcome />
    <Courses />
    <Teachers />
    <Reviews />
    <Feedback />
    <Contacts />
  </main>
  <footer class="footer relative">
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

<style lang="scss">
@font-face {
  font-family: "Uncage";
  src: url(/fonts/UNCAGE-SemiBold.ttf);
}

@font-face {
  font-family: "AcherusFeral-Bold";
  src: url(/fonts/AcherusFeral-Bold.otf);
}

@font-face {
  font-family: "AcherusFeral-Light";
  src: url(/fonts/AcherusFeral-Light.otf);
}

@font-face {
  font-family: "UnboundedRegular";
  src: url(/public/fonts/Unbounded-Regular.ttf);
}

@font-face {
  font-family: "UnboundedSemiBold";
  src: url(/public/fonts/Unbounded-SemiBold.ttf);
}

.mainStyle {
  display: flex;
  flex-direction: column;
  gap: 200px;
}

h1 {
  font-family: "Uncage";
  font-size: 50px;
  text-transform: uppercase;
}

h5 {
  font-family: "AcherusFeral-Light";
  font-size: 25px;
}

h2 {
  font-family: "AcherusFeral-Light";
  font-size: 30px;
}

header {
  margin-left: 40px;
  margin-right: 40px;
  height: 143px;
}

.social-links {
  @apply flex gap-4;

  a,
  img {
    width: 30px;
    height: 30px;

    &:hover {
      transition: all 0.2s;
      transform: scale(1.2);
    }
  }
}

.navigate {
  @apply flex w-full;
  justify-content: center;
  column-gap: 30px;
  a {
    margin-left: 10px;
    margin-right: 10px;
    font-size: 1.5vw;
    text-transform: uppercase;
    font-family: "Uncage";

    &:hover {
      color: #328862;
    }
  }
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
