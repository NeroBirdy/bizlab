<script setup lang="ts">
import axios from "axios";
import { ref } from "vue";

const email = ref<string>("");
const pass = ref<string>("");
const errorMessage = ref<string>("");

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const userInfo = useAuthStore();

const goHome = () => {
  navigateTo("/");
};

const validateForm = (): boolean => {
  if (!email.value.trim()) {
    errorMessage.value = "Поле 'почта' не может быть пустым.";
    return false;
  }

  if (!pass.value.trim()) {
    errorMessage.value = "Поле 'пароль' не может быть пустым.";
    return false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.value)) {
    errorMessage.value = "Введите корректный адрес электронной почты.";
    return false;
  }

  if (pass.value.length < 6) {
    errorMessage.value = "Пароль должен содержать минимум 6 символов.";
    return false;
  }

  errorMessage.value = "";
  return true;
};

const login = async () => {
  try {
    if (!validateForm()) {
      return;
    }

    const formData = {
      email: email.value,
      password: pass.value,
    };

    const response = await axios.post(`${apiBase}/api/auth/login`, formData);
    const authToken = useCookie("auth_token", {
      httpOnly: false,
      secure: true,
      sameSite: "strict",
      maxAge: 300,
    });
    const refreshToken = useCookie("refresh_token", {
      httpOnly: false,
      secure: true,
      sameSite: "strict",
      maxAge: 86400,
    });

    authToken.value = response.data.tokens.access;
    refreshToken.value = response.data.tokens.refresh;
    userInfo.loginUser();
  } catch (error: any) {
    if (error.response) {
      errorMessage.value = "Что-то не совпадает, проверьте свои данные";
    } else {
      console.error(error);
      alert("Произошла ошибка при отправке запроса.");
    }
  }
};

onMounted(() => {
  if (userInfo.isAuth) {
    navigateTo("/course");
  }
});
</script>

<template>
  <div class="back-image">
    <img class="back" src="../../assets/images/back-login.svg" alt="" />
  </div>
  <div class="log-form">
    <div class="logo flex" @click="goHome()">
      <img
        class="h-12 self-center"
        src="../../assets/images/bizlap-logo.svg"
        alt="Logo"
      />
      <h1 class="mb-10">АВТОРИЗАЦИЯ</h1>
    </div>
    <form @submit.prevent="login" class="login-form">
      <input
        type="email"
        placeholder="E-mail"
        v-model="email"
        class="input"
        required
      />
      <input
        type="password"
        placeholder="Пароль"
        v-model="pass"
        class="input"
        required
      />
      <div v-if="errorMessage" class="error-message text-red-500 text-sm">
        {{ errorMessage }}
      </div>
      <div class="flex justify-center">
        <button type="submit" class="btn log">вход</button>
      </div>
    </form>
  </div>
</template>

<style lang="scss" scoped>
@use "~/assets/scss/main.scss" as main;
@use "sass:color";
.back {
  opacity: 30%;
  scale: 0.8;
}

h1 {
  text-align: center;
  color: #328862;
  display: flex;
  letter-spacing: 2px;
  justify-content: center;
  width: 100%;
  font-family: "Inter";
  font-weight: 600;
  font-size: 28px;
}

p {
  margin-left: 1rem;
  color: main.$primary-color;
  font-weight: bold;
}

.logo {
  justify-content: center;
  flex-direction: column;
}

.login-form {
  @apply flex flex-col space-y-1 self-center;
  width: 70%;
  align-items: center;
}

.back-image {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  width: 100%;
}
input {
  border: 2px solid #328862;
  font-size: 20px;
  width: 70%;
  padding-left: 15px;
  background-color: white;
  border-radius: 20px;
  font-family: "Inter";
  &::placeholder {
    color: #328862;
    font-weight: 600;
  }

  &:focus {
    background-color: white;
    color: black;
    border: 3px solid #46c089;
    outline: none;

    &::placeholder {
      color: #46c089;
    }
  }
}

.btn {
  width: 130px !important;
  font-weight: 600;
  text-align: center;
  align-items: center;
  font-size: 20px;
  border-radius: 30px;
}

.log {
  background-color: #3840a9;
  width: 100%;
  color: white;
  font-family: "Uncage";

  &:hover {
    background-color: color.adjust(#3840a9, $lightness: -5%);
  }
}

.log-form {
  @apply flex items-center;
  flex-direction: column;
  width: 70%;
  margin: auto;
  margin-top: 30px;
  position: relative;
  top: calc(100vh / 4);
  border-radius: 10px;
  height: 180px;
}

.error-message {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: red;
}

@media (min-width: 1600px) {
  .log-form {
    width: 50%;
  }
}

@media (max-width: 1024px) {
  .input {
    height: 50px;
    width: 450px;
  }

  .btn {
    height: 50px;
  }
}

@media (max-width: 768px) {
  .back {
    scale: 1;
  }
  .input {
    width: 400px;
  }
}

@media (max-width: 425px) {
  .input {
    width: 300px;
  }

  .back {
    scale: 2;
  }
}
</style>
