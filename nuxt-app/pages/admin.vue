<template>
  <div>
    <header class="flex w-full h-full justify-between items-center relative">
      <img class="logo" src="/assets/images/bizlap-logo.svg" alt="bizlab" />
      <h1>АДМИНИСТРАТОР</h1>
      <p>выйти из личного кабинета</p>
    </header>
  </div>
  <div>
    <button class="btn btn-primary" @click="openRegisterTeacherModal">
      добавить преподавателя
    </button>
    <AddTeacher ref="registerTeacherRef" />
    <button class="btn btn-secondary" @click="openDeleteTeacherModal">
      удалить преподавателя
    </button>
    <deleteTeacher ref="deleteTeacherRef" />
  </div>
  <div>
    <form @submit.prevent="handlerComment">
      <label for="sender">Отправитель:</label>
      <input type="text" id="sender" v-model="sender" required />
      <label for="comment">Текст комментария:</label>
      <input id="comment" v-model="text" required />
      <button type="submit">Отправить</button>
    </form>
  </div>
  <div></div>
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

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

const openDeleteTeacherModal = () => {
  deleteTeacherRef.value?.openModal();
};

const openRegisterTeacherModal = () => {
  registerTeacherRef.value?.openModal();
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
input {
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
</style>
