<template>
  <div class="contactsContent">
    <h1 class="flex justify-center">
      <span class="highlight">Контакты </span> центра
    </h1>
    <div class="contacts-block">
      <div class="contacts">
        <div class="contacts-top">
          <div class="contacts-left">
            <img src="/assets/images/welcomePage/jababa.png" class="leftFrog"/>
            <div class="contact-container">
              <div class="text-area">
                <h2>Находимся по адресу:</h2>
                <p>г. Ханты-Мансийск,</p>
                <p>ул. Свердлова д. 28</p>
              </div>
            </div>
          </div>
          <img src="/assets/images/welcomePage/zigzak.png" class="glist" />
          <div class="contacts-right">
            <div class="contact-container">
              <div class="text-area">
                <h2>Электронная почта:</h2>
                <p>perezagruxkahm@mail.ru</p>
                <h2>Наш телефон:</h2>
                <p>+7 952 702 50 50</p>
              </div>
            </div>
            <img src="/assets/images/welcomePage/jababa.png" class="rightFrog"/>
          </div>
        </div>
        <div class="contacts-bottom">
          <div class="flex contact-card justify-center last-block">
            <div class="contact-container vk-block">
              <h2>Можете следить за нашими нововостями в группе ВКонтакте</h2>
              <div class="flex justify-center">
                <img src="/assets/images/links/vk.svg" />
                <p>Образовательная лаборатория “BizLab”</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>   
  </div>
</template>

<script setup></script>

<style lang="scss" scoped>
h1 {
  font-size: 3.5vw;
  margin-bottom: 5vw;
  // margin-top: 15vw;
  gap: 2.5vw;
}

.highlight {
  color: rgb(226, 93, 53);
}

.contactsContent {
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.contacts-block {
  display: flex;
  flex-direction: row;
  width: 90%;
}

.contacts {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.contacts-top {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: top;
  width: 100%;
  height: 20vw;
}

.contacts-left, .contacts-right {
  display: flex;
  justify-content: center;
  img {
    position: relative;
    object-fit: contain;
    width: 30%;
  }
}

.contacts-left {
  img {
    right: -5%;
  }
}

.contacts-right {
  img {
    transform: scale(-1, 1);
    left: -5%;
  }
}

.text-area {
  width: 99%;
}

.glist {
  transform: scale(calc(100vw * 100));
  object-position: top;
  position: relative;
  top: -20%;
}

// .container {
//   width: 80%;
// }

.contact-container {
  display: flex;
  gap: 1vw;
  background-color: #f0ac02;
  width: 65%;
  border-radius: 3.5vw;
  height: 15.6vw;
  padding: 1.7vw;
  text-align: center;

  h2 {
    color: white;
    font-family: "UnboundedSemiBold";
    font-size: 1.6vw;
  }

  p {
    font-family: "UnboundedRegular";
    font-size: 1.2vw;
    line-height: 1.5vw;
    color: white;
  }
}

.contacts-left {
  .contact-container{
    img {
      left: -35%;
    }
  }
}

.vk-block {
  width: 34.7vw;
  display: flex;
  flex-direction: column;
  h2 {
    text-align: center;
    font-size: 1.4vw;
  }

  img {
    display: block;
    width: 7vw;
    height: 4.8vw;
    display: flex;
  }

  p {
    display: flex;
    width: 70%;
    height: 4.8vw;
    align-items: center;
  }
}

@media (max-width: 425px) {
  h1 {
      gap: 1.5vw;
  }
  .vk-block {
    width: 60vw;
    justify-content: center;
    h2 {
      font-size: 2vw;
      line-height: 2.3vw;
    }

    p {
      font-size: 2vw;
      line-height: 2vw;
    }
  }
  .glist {
    display: none;
  }
  .contacts-top {
    flex-direction: column;
    height: 45vw;
  }
  .contacts-bottom {
    margin-top: 10vw;
    width: 100%;
  }
  .contacts-left, .contacts-right {
    img {
      width: 20%;
    }
  .contact-container {
    padding: 2vw;
    h2 {
      font-size: 2.5vw;
    }

    p {
      font-size: 2vw;
      line-height: 2vw;
    }
  }
}
}
</style>
<script setup>
import { onMounted, onBeforeUnmount } from 'vue'

function updateGListScale() {
  const glist = document.querySelector('.glist')
  const rightFrog = document.querySelector('.rightFrog')
  const leftFrog = document.querySelector('.leftFrog')
  if (!glist) return

  const width = window.innerWidth

  if (width <= 1440) {
    const scaleValue = width / 1440
    const top = 10 * ((1 - scaleValue) + 1)
    const vertical = 0.52 * ((1 - scaleValue) * 100)
    glist.style.transform = `scale(${scaleValue})`
    glist.style.top = `-${top}%`
  }
  // rightFrog.style.top = `-${vertical}%`
  // leftFrog.style.top = `-${vertical}%`
}

onMounted(() => {
  updateGListScale()
  window.addEventListener('resize', updateGListScale)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', updateGListScale)
})
</script>