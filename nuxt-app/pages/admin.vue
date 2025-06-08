<template>
  <BizlabLogo />
  <p class="logout" @click="logout">ВЫЙТИ ИЗ ЛИЧНОГО КАБИНЕТА</p>
  <div class="window-card">
    <div class="admin-card">
      <header class="header">
        <h1>АДМИНИСТРАТОР</h1>
      </header>
      <div class="buttons-div">
        <button class="btn bg-[#328862]" @click="openRegisterTeacherModal">
          добавить преподавателя
        </button>
        <AddTeacher ref="registerTeacherRef" />
        <button class="btn bg-[#E15D34]" @click="openDeleteTeacherModal">
          удалить преподавателя
        </button>
        <deleteTeacher ref="deleteTeacherRef" />
      </div>
      <div class="flex justify-center flex-col">
        <h2>Создание отзывов</h2>
        <form @submit.prevent="handlerComment" class="flex flex-col">
          <label for="sender" class="form-title">Отправитель:</label>
          <input type="text" id="sender" v-model="sender" required />
          <label for="comment" class="form-title">Текст комментария:</label>
          <textarea id="comment" v-model="text" required class="textarea" />
          <div class="flex justify-end">
            <button type="submit" class="btn bg-[#3840A9] w-40 mt-5">
              Отправить
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import deleteTeacher from "../components/deleteTeacher.vue";
import AddTeacher from "../components/AddTeacher.vue";

const deleteTeacherRef = ref();
const registerTeacherRef = ref();
const sender = ref();
const text = ref();
const userStore = useAuthStore();
const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

const openDeleteTeacherModal = () => {
  deleteTeacherRef.value?.openModal();
};

const openRegisterTeacherModal = () => {
  registerTeacherRef.value?.openModal();
};

const logout = async () => {
  //   const response = await axios.post(`${apiBase}/api/auth/logout`);
  userStore.logoutUser();
  navigateTo("/");
};

const handlerComment = async () => {
  try {
    const form = new FormData();

    form.append("sender", sender.value);
    form.append("text", text.value);

    const response = await axios.post(`${apiBase}/api/createComment`, form);

    console.log("Комментарий успешно создан:", response.data);
    alert("Комментарий успешно создан!");
    sender.value = "";
    text.value = "";
  } catch (error) {
    console.error("Ошибка при создании комментария:", error);
    alert("Ошибка при создании комментария. Пожалуйста, попробуйте снова.");
  }
};
</script>

<style lang="scss" scoped>
input,
textarea {
  @apply shadow-md;
  height: 30px;
  padding: 5px;
  font-size: 1vw;
  border: 2px solid green;
  border-radius: 5px;
  margin-top: 5px;
  background-color: white;
  &::placeholder {
    color: green;
  }
}

textarea {
  min-height: 30px;
  height: 200px;
}

.buttons-div {
  display: flex;
  justify-content: space-evenly;
  padding-bottom: 10px;
  border-bottom: 1px solid #ccc;
  margin-bottom: 10px;
}

.logout {
  cursor: pointer;
  position: absolute;
  top: 2%;
  right: 2%;
  display: flex;
  width: 100px;
  font-family: "Uncage";
  color: #e15d34;
  transition: all 0.5s;
  &:hover {
    transform: translateX(-10px);
  }
}

.window-card {
  width: 1000px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.admin-card {
  background-color: rgb(223, 235, 247);
  width: 100% !important;
  padding: 15px 30px;
  border-radius: 5px;
  transition: transform 0.2s ease-in-out;
  width: calc(50% - 10px);
  cursor: pointer;
}

.header {
  height: max-content;
  display: flex;
  margin: 0;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  width: 100%;
  border-bottom: 1px solid #ccc;
  margin-bottom: 10px;

  h1 {
    font-family: "Uncage";
    font-size: 24px;
  }
}

.btn {
  font-family: "Uncage";
  font-size: 18px;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 25px;
  cursor: pointer;

  transition: all 0.2s;
  &:hover {
    transform: translateY(-5px) scale(1.05);
    opacity: 70%;
  }
}

h2 {
  font-family: "Uncage";
  font-size: 24px;
}

.form-title {
  font-family: "Itern";
  font-size: 20px;
}
</style>
