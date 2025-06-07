<template>
  <div class="relative">
    <img
      src="/assets/images/teachersPage/vectorStar.svg"
      alt="Star"
      class="star2"
    />
    <img
      src="/assets/images/teachersPage/vectorWave.svg"
      alt="Wave"
      class="wave2"
    />
    <div class="container flex relative">
      <img
        src="/assets/images/welcomePage/callback.png
    "
        class="bg-card"
      />
      <div class="form-div">
        <form @submit.prevent="sendRequest" class="">
          <h3>ЗАПОЛНЯЙ АНКЕТУ</h3>
          <div class="mt-10 input-div">
            <input type="text" placeholder="ФИО" />
            <input type="text" placeholder="Телефон" />
          </div>
          <div class="mt-10 checkbox-div">
            <div>
              <div class="checkbox-wrapper">
                <input type="checkbox" id="check" />
              </div>
            </div>
            <label for="check" class="block">
              Нажимая кнопку, вы даете согласие на обработку личных данных
            </label>
          </div>
          <button type="submit" class="btn">ОТПРАВИТЬ</button>
          <NuxtLink
            :to="userInfo.isAuth ? '/course' : '/auth/login'"
            class="self-center"
          >
            уже с нами?
          </NuxtLink>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;
const userInfo = useAuthStore();
const fio = ref();
const number = ref();

const sendRequest = async () => {
  const form = new FormData();

  try {
    form.append("fio", fio.value);
    form.append("number", number.value);
    const response = await axios.post(`${apiBase}/api/sendEmailToAdmin`, form);
    alert("Запрос успешно отправлен!");
  } catch (error) {
    console.log("Ошибка", error);
  }
};
</script>

<style lang="scss" scoped>
.bg-card {
  width: 80%;
}

.form-div {
  position: absolute;
  height: 120%;
  border: #2b7454 10px solid;
  background-color: white;
  right: 0;
  top: -50px;
  width: 500px;
  border-radius: 50px;
}

form {
  display: flex;
  width: 100%;
  flex-direction: column;
  justify-content: center;
  h3 {
    margin-top: 10%;
    width: 100%;
    text-align: center;
    word-spacing: 100px;
    font-family: "UnboundedSemiBold";
    font-size: 32px;
    color: #e15d34;
  }
  .input-div {
    display: flex;
    flex-direction: column;
    width: 100%;
    justify-content: center;
    input[type="text"] {
      width: 80%;
      margin-right: auto;
      margin-left: auto;
      @apply shadow-md;
      padding: 5px;
      font-size: 1.5vw;
      border: 5px solid #2b7454;
      border-radius: 15px;
      margin-top: 35px;
      background-color: white;
      &::placeholder {
        color: #2b7454;
      }
    }
  }
  .btn {
    margin-top: 40px;
    margin-left: auto;
    margin-right: auto;
    width: 230px;
    border-radius: 50px;
    height: 80px;
    color: white;
    font-family: "Uncage";
    background-color: #e25d35;
  }

  .checkbox-wrapper {
    display: inline-flex;
    position: relative;
    margin: 0;
    margin-right: 20px;
    padding: 0;
    accent-color: #2b7454;
    width: 40px;
    height: 40px;
  }

  .checkbox-wrapper input[type="checkbox"] {
    position: absolute;
    top: 0;
    left: 0;
    opacity: 1;
    width: 100%;
    height: 100%;
    margin: 0;
    padding: 0;
    cursor: pointer;
  }

  .checkbox-wrapper::after {
    content: "";
    position: absolute;
    top: 0px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    border: 4px solid green;
    border-radius: 4px;
    pointer-events: none;
    box-sizing: border-box;
    z-index: 1;
  }
}

.checkbox-div {
  display: flex;
  width: 80%;
  margin-right: auto;
  margin-left: auto;
}

.star2,
.wave2 {
  position: absolute;
  z-index: -1;
}

.star2 {
  top: 0;
  right: 0;
}

.wave2 {
  left: -160px;
  top: -120px;
  height: 700px;
}
</style>
