<template>
  <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
    <div class="modal">
      <h1>Создание урока</h1>

      <!-- Поле ввода -->
      <input
        ref="lessonNameInput"
        type="text"
        v-model="newLessonName"
        placeholder="Введите название урока"
        @keydown.enter="createLesson"
      />

      <!-- Кнопки управления -->
      <div class="modal-buttons">
        <button @click="closeModal">Отмена</button>
        <button @click="createLesson" :disabled="!newLessonName">
          Создать
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, defineExpose, nextTick } from "vue";
import axios from "axios";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

// === Props ===
const props = defineProps<{
  courseId: number;
}>();

// === Emits ===
const emit = defineEmits<{
  (e: "lesson-created", lessonName: string): void;
}>();

// === Локальное состояние ===
const showModal = ref(false);
const newLessonName = ref("");
const lessonNameInput = ref<HTMLInputElement | null>(null);

// === Открытие/закрытие модального окна ===
const openModal = () => {
  showModal.value = true;
  newLessonName.value = "";
  nextTick(() => {
    lessonNameInput.value?.focus();
  });
};

const closeModal = () => {
  showModal.value = false;
  newLessonName.value = "";
};

// === Создание урока ===
const createLesson = async () => {
  if (!newLessonName.value.trim()) return;

  try {
    const response = await axios.post(`${apiBase}/api/createTask`, {
      courseId: props.courseId,
      name: newLessonName.value,
    });

    const newLessonNameResult = response.data.lessonName || newLessonName.value;

    closeModal();
    emit("lesson-created", newLessonNameResult);
  } catch (error) {
    console.error("Ошибка при создании урока:", error);
    alert("Не удалось создать урок");
  }
};

// === Экспорт методов для вызова извне ===
defineExpose({ openModal });
</script>

<style lang="scss" scoped>
h1 {
  font-size: 24px;
  font-family: "Uncage";
}

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

.modal input {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  margin-bottom: 10px;
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
