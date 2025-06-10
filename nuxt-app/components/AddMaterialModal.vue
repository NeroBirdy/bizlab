<template>
  <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
    <div class="modal">
      <h1>Добавление материала</h1>

      <!-- Выбор урока -->
      <label for="lessonSelect">Выберите урок:</label>
      <select id="lessonSelect" v-model="selectedLessonId" required>
        <option disabled value="">-- Выберите урок --</option>
        {{
          course
        }}
        <option
          v-for="(lesson, lessonId) in course"
          :key="lessonId"
          :value="lessonId"
        >
          {{ lesson.name }}
        </option>
      </select>

      <!-- Выбор типа материала -->
      <label for="materialType">Тип материала:</label>
      <select id="materialType" v-model="selectedType">
        <option value="1">Учебный материал</option>
        <option value="2">Домашняя работа</option>
        <option value="3">Тест</option>
        <option value="4">Ссылка</option>
      </select>

      <!-- Название материала -->
      <label for="materialName">Название материала:</label>
      <input
        id="materialName"
        type="text"
        v-model="newMaterialName"
        placeholder="Введите название материала"
      />

      <!-- Файл/ссылка в зависимости от типа -->
      <div v-if="selectedType !== '4'">
        <label for="fileInput">Выберите файл:</label>
        <input
          id="fileInput"
          type="file"
          ref="fileInput"
          @change="handleFileUpload"
        />
      </div>
      <div v-else>
        <label for="linkInput">Введите ссылку:</label>
        <input
          id="linkInput"
          type="text"
          v-model="newLink"
          placeholder="https://example.com "
        />
      </div>

      <!-- Кнопки управления -->
      <div class="modal-buttons">
        <button @click="closeModal">Отмена</button>
        <button @click="createMaterial" :disabled="!isValidForm">
          Создать материал
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineExpose, defineEmits } from "vue";
import axios from "axios";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

// === Props ===
const props = defineProps<{
  course: {
    [lessonId: number]: {
      id: number;
      name: string;
      materials: {
        id: number;
        name: string;
        type: string;
      }[];
    };
  };
  courseId: number;
}>();

// === Emits ===
const emit = defineEmits<{
  (
    e: "material-created",
    lessonId: number,
    material: {
      id: number;
      name: string;
      type: string;
      file?: string;
      link?: string;
    }
  ): void;
}>();

// === Локальное состояние ===
const showModal = ref(false);
const selectedLessonId = ref<number | null>(null);
const selectedType = ref("1");
const newMaterialName = ref("");
const newLink = ref("");
const fileInput = ref<HTMLInputElement | null>(null);

// === Проверка формы ===
const isValidForm = computed(() => {
  if (!selectedLessonId.value) return false;
  if (!newMaterialName.value.trim()) return false;

  if (selectedType.value === "4") {
    return !!newLink.value.trim();
  }

  return !!fileInput.value?.files?.length;
});

// === Обработка загрузки файла ===
const handleFileUpload = () => {
  const file = fileInput.value?.files?.[0];
  if (file) {
    console.log("Файл выбран:", file.name);
  }
};

// === Создание материала ===
const createMaterial = async () => {
  try {
    const formData = new FormData();
    const lessonName = props.course[selectedLessonId.value!].name;
    const lessonId = props.course[selectedLessonId.value!].id;
    formData.append("courseId", props.courseId.toString());
    formData.append("lessonName", lessonName);
    formData.append("type", selectedType.value);
    formData.append("name", newMaterialName.value);

    if (selectedType.value === "4") {
      formData.append("link", newLink.value);
    } else {
      const file = fileInput.value?.files?.[0];
      if (file) {
        formData.append("file", file);
      }
    }

    const response = await axios.post(
      `${apiBase}/api/createMaterial`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    closeModal();
    emit("material-created", lessonId, response.data.material);
  } catch (error) {
    if (error.response.data.message == "Материал с таким названием уже есть") {
      alert("Материал с таким названием уже есть");
    } else {
      console.error("Ошибка при создании материала:", error);
      alert("Не удалось создать материал");
    }
  }
};

// === Открытие/закрытие модального окна ===
const openModal = () => {
  showModal.value = true;
  nextTick(() => {
    fileInput.value && (fileInput.value.value = "");
  });
};

const closeModal = () => {
  showModal.value = false;
  selectedLessonId.value = null;
  selectedType.value = "1";
  newMaterialName.value = "";
  newLink.value = "";
  fileInput.value && (fileInput.value.value = "");
};

// === Экспорт методов для вызова извне ===
defineExpose({ openModal });
</script>

<style scoped>
h1 {
  text-align: center;
  font-size: 18px;
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

.modal label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.modal input,
.modal select {
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
