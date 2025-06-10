<template>
  <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
    <div class="modal">
      <h3>Регистрация учителя</h3>

      <!-- Фамилия -->
      <label for="lastName">Фамилия:</label>
      <input
        id="lastName"
        type="text"
        v-model="lastName"
        placeholder="Введите фамилию"
        required
      />

      <!-- Имя -->
      <label for="firstName">Имя:</label>
      <input
        id="firstName"
        type="text"
        v-model="firstName"
        placeholder="Введите имя"
        required
      />

      <!-- Отчество -->
      <label for="secondName">Отчество:</label>
      <input
        id="secondName"
        type="text"
        v-model="secondName"
        placeholder="Введите отчество"
        required
      />

      <!-- Почта -->
      <label for="email">Почта:</label>
      <input
        id="email"
        type="email"
        v-model="email"
        placeholder="Введите email"
        required
      />

      <!-- Кнопки управления -->
      <div class="modal-buttons">
        <button @click="closeModal">Отмена</button>
        <button @click="registerTeacher" :disabled="!isValidForm">
          Зарегистрировать
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineExpose } from "vue";
import axios from "axios";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

// === Локальное состояние ===
const showModal = ref(false);
const firstName = ref("");
const secondName = ref("");
const lastName = ref("");
const email = ref("");

// === Проверка формы ===
const isValidForm = computed(() => {
  return (
    firstName.value.trim() &&
    secondName.value.trim() &&
    lastName.value.trim() &&
    email.value.trim()
  );
});

// === Регистрация учителя ===
const registerTeacher = async () => {
  try {
    const response = await axios.post(`${apiBase}/api/auth/registration`, {
      firstName: firstName.value,
      secondName: secondName.value,
      lastName: lastName.value,
      email: email.value,
      role: 1,
    });

    closeModal();
    alert("Учитель успешно зарегистрирован");
  } catch (error) {
    console.error("Ошибка при регистрации учителя:", error);
    alert("Не удалось зарегистрировать учителя");
  }
};

// === Открытие/закрытие модального окна ===
const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  firstName.value = "";
  secondName.value = "";
  lastName.value = "";
  email.value = "";
};

// === Экспорт методов для вызова извне ===
defineExpose({ openModal });
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
  position: relative;
}

.modal label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.modal input {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 10px;
}

.modal-buttons button {
  padding: 10px 20px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal-buttons button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}
</style>
