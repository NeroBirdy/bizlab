<script setup lang="ts">
import { ClientOnly } from "#components";
</script>

<template>
  <header>
    <div class="flex w-full h-full justify-between items-center relative header-desktop">
      <div class="logo-box">
        <img class="logo" src="/assets/images/bizlap-logo.svg" alt="bizlab" />
      </div>
      <!-- <img class="logo" src="/assets/images/bizlap-logo.svg" alt="bizlab" /> -->
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
    <div class="header-mobile">
      <div class="header-mobile-container">
        <img class="logo" src="/assets/images/bizlap-logo.svg" alt="bizlab" />
        <div class="menu">
            <input type="checkbox" id="burger-checkbox" class="burger-checkbox">
            <label for="burger-checkbox" class="burger"></label>
            <ul class="menu-list">
                <li><a href="#" class="menu-item">О нас</a></li>
                <li><a href="#" class="menu-item">Курсы</a></li>
                <li><a href="#" class="menu-item">Команда</a></li>
                <li><a href="#" class="menu-item">Отзывы</a></li>
                <li><a href="#" class="menu-item">Записаться</a></li>
                <li><a href="#" class="menu-item">Контакты</a></li>
            </ul>
        </div>
      </div>
    </div>
  </header>
  <div class="area">
    <Welcome />
    <Courses />
    <Teachers />
    <Reviews />
    <Feedback/>
    <Contacts />
  </div>
</template>

<style lang="scss">

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}

.area {
  margin: 0;
  padding: 0;
  width: 100%;
  max-width: 100%;
}

.content {
  height: 90vh;
  width: 100vw;
  // overflow: hidden;
  margin-bottom: 15vh;
}

.content-mobile {
  // height: 50vh;
  // overflow: hidden;
  margin-bottom: 15vh;
}

.mainStyle {
  display: flex;
  flex-direction: column;
  gap: 3vw;
}

h1 {
  font-family: "Uncage";
  font-size: 3.5vw;
  text-transform: uppercase;
}

h5 {
  font-family: "AcherusFeral-Light";
  font-size: 1.7vw;
}

h2 {
  font-family: "AcherusFeral-Light";
  font-size: 2vw;
}

header {
  margin-left: 5vw;
  margin-right: 5vw;
  height: 10vh;
}

.social-links {
  @apply flex gap-4;

  a,
  img {
    width: auto;
    height: 3vw;

    &:hover {
      transition: all 0.2s;
      transform: scale(1.2);
    }
  }
}

.navigate {
  @apply flex w-full;
  justify-content: center;
  column-gap: 1vw;
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

.menu {
  z-index: 3;
}

.burger-checkbox {
  position: absolute;
  visibility: hidden;
}
.burger {
  position: relative;
  z-index: 1;
  cursor: pointer;
  display: block;
  position: relative;
  border: none;
  background: transparent;
  width: 40px;
  height: 26px;
}
.burger::before,
.burger::after {
  content: '';
  left: 0;
  position: absolute;
  display: block;
  width: 100%;
  height: 4px;
  border-radius: 10px;
  background: #000;
}
.burger::before {
  top: 0;
  box-shadow: 0 11px 0 #000;
  transition: box-shadow .3s .15s, top .3s .15s, transform .3s;
}
.burger::after {
  bottom: 0;
  transition: bottom .3s .15s, transform .3s;
}
.burger-checkbox:checked + .burger::before {
  top: 11px;
  transform: rotate(45deg);
  box-shadow: 0 6px 0 rgba(0,0,0,0);
  transition: box-shadow .15s, top .3s, transform .3s .15s;
}
.burger-checkbox:checked + .burger::after {
  bottom: 11px;
  transform: rotate(-45deg);
  transition: bottom .3s, transform .3s .15s;
}
.menu-list {
  top: 0;
  left: 0;
  position: absolute;
  padding: 42px 0;
  margin: 0;
  background: rgb(50, 136, 98);
  list-style-type: none;
  transform: translateX(-100%);
  transition: .3s;
  width: 100vw;
  height: 100vh;
}

.menu-list {
  li {
    height: 7vh;
  }
}

.menu-item {
  display: block;
  padding: 8px;
  color: white;
  font-size: 18px;
  text-align: center;
  text-decoration: none;
  font-family: "Uncage";
}
.menu-item:hover {
  background: rgba(255,255,255,.2)
}
.burger-checkbox:checked ~ .menu-list {
  transform: translateX(0);
}

.logo {
  width: 17vw;
}

.header-mobile {
  width: 100%;
  height: 100%;
  display: none;
}

.header-mobile-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

@media (max-width: 980px) {
  .navigate {
    a {
      font-size: 1.3vw;
    }
  }
}

@media (max-width: 767px) {
  .header-desktop {
    display: none;
  }
  .header-mobile {
    display: block;
  }
  .logo {
    width: 40vw;
  }
}

@media (max-width: 1023px) {
  .content {
    height: 75vh;
  }
}

@media (max-width: 425px) {
  .content {
    height: 90vh;
  }
  h1 {
    font-size: 6vw;
  }
  h2 {
    font-size: 5vw;
  }
  h5 {
    font-size: 4vw;
  }
}
</style>
