<template>
  <div class="feedbackContent"  id="feedback">
    <!-- <img
      src="/assets/images/teachersPage/vectorStar.svg"
      alt="Star"
      class="star2"
    />
    <img
      src="/assets/images/teachersPage/vectorWave.svg"
      alt="Wave"
      class="wave2"
    /> -->
    <div class="feedback-block">
      <div class="form-div">
        <form @submit.prevent="sendRequest" class="">
          <h3>ЗАПОЛНЯЙ АНКЕТУ</h3>
          <div class="input-div">
            <input type="text" placeholder="ФИО" />
            <input type="text" placeholder="Телефон" />
          </div>
          <div class="checkbox-div">
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
.feedbackContent {
  width: 100vw;
  height: 90vw;
  display: flex;
  justify-content: center;
  align-items: center;
}

.feedback-block {
  background-image: url("/assets/images/welcomePage/callback.png");
  background-repeat: no-repeat;
  background-size: contain;
  width: 78%;
  height: 40%;
  display: flex;
  justify-content: end;
}

.bg-card {
  width: 80%;
}

.form-div {
  height: 130%;
  width: 50%;
  border: #2b7454 0.7vw solid;
  background-color: white;
  border-radius: 3.5vw;
  position: relative;
  top: -15%;
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
    // word-spacing: 100px;
    font-family: "UnboundedSemiBold";
    font-size: 2.2vw;
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
      padding: 0.35vw;
      font-size: 1.5vw;
      border: 0.35vw solid #2b7454;
      border-radius: 1vw;
      margin-top: 2.5vw;
      background-color: white;
      &::placeholder {
        color: #2b7454;
      }
    }
  }
  .btn {
    margin-top: 2.7vw;
    margin-left: auto;
    margin-right: auto;
    width: 16vw;
    border-radius: 3.5vw;
    height: 5.5vw;
    color: white;
    font-family: "Uncage";
    background-color: #e25d35;
    font-size: 1.4vw;
  }

  .checkbox-wrapper {
    display: inline-flex;
    position: relative;
    margin: 0;
    margin-right: 1.4vw;
    padding: 0;
    accent-color: #2b7454;
    width: 2.7vw;
    height: 2.7vw;
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
    border: 0.27vw solid green;
    border-radius: 4px;
    pointer-events: none;
    box-sizing: border-box;
    z-index: 1;
  }

  label {
    font-size: 1.1vw;
  }

  a {
    font-size: 1.1vw;
  }
}

.checkbox-div {
  display: flex;
  width: 80%;
  margin-right: auto;
  margin-left: auto;
  margin-top: 3vw;
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

@media (max-width: 768px) {
  form {
    label {
      font-size: 1.3vw;
    }
    a {
      font-size: 1.3vw;
    }
  }
}

@media (max-width: 425px) {
  form {
    label {
      font-size: 1.6vw;
    }
    a {
      font-size: 1.6vw;
    }
    .input-div {
      margin-top: 3vw;
    }
  }
  .feedback-block {
    background-image: none;
    justify-content: center;
  }
  .form-div {
    scale: 2;
    height: 150%;
    background-color: #f3f3f3;
  }

  .feedbackContent{
    margin-bottom: 10vh;
  }  
}
</style>
