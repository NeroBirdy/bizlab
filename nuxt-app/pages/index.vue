<script setup lang="ts">
import { ClientOnly } from "#components";
</script>

<template>
  <ClientOnly>
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
  </ClientOnly>
</template>

<style lang="scss">
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
</style>
