<template>
  <Backimages :variable="2" />
  <img src="/assets/images/bizlap-logo.svg" alt="logo" class="bizlab-logo" />
  <div class="course-page">
    <header class="header">
      <h1>{{ courseName }}</h1>
      <nav>
        <button
          @click="chooseHomework = false"
          :class="{ active: !chooseHomework }"
        >
          Учебные материалы
        </button>
        <button
          @click="chooseHomework = true"
          :class="{ active: chooseHomework }"
        >
          Домашние работы
        </button>
      </nav>
    </header>

    <!-- Основной контент -->
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else>
      <!-- Вкладка: Учебные материалы -->
      <div v-if="!chooseHomework" class="materials-view">
        <div class="actions">
          <button class="create-lesson" @click="openAddLessonModal">
            Создать урок
          </button>
          <AddLessonModal
            ref="addLessonModal"
            :courseId="courseId"
            @lesson-created="onLessonCreated"
          />
          <button class="upload-material" @click="openAddMaterialModal">
            Загрузить материал
          </button>

          <!-- Подключение модала -->
          <AddMaterialModal
            ref="addMaterialModal"
            :course="course"
            :courseId="courseId"
            @material-created="onMaterialCreated"
          />
        </div>
        <!-- Список уроков -->
        <div v-if="course" class="lessons-container">
          <div
            v-for="(materials, lessonName) in course"
            :key="lessonName"
            class="lesson-card"
          >
            <div class="lesson-header">
              <!-- Режим редактирования -->
              <div v-if="editingLesson === lessonName" class="edit-mode">
                <input
                  v-model="editedLessonName"
                  type="text"
                  placeholder="Название урока"
                  class="lesson-name-input"
                />
                <button @click="saveLesson(lessonName)" class="save-button">
                  Сохранить
                </button>
              </div>

              <!-- Обычный режим -->
              <span v-else>{{ lessonName }}</span>

              <!-- Кнопки управления -->
              <div class="lesson-actions">
                <button
                  v-if="editingLesson !== lessonName"
                  @click="editLesson(lessonName)"
                  class="edit-button"
                >
                  Редактировать
                </button>
                <button
                  v-if="editingLesson === lessonName"
                  @click="removeLesson(lessonName)"
                  class="delete-button"
                >
                  Удалить
                </button>
              </div>
            </div>

            <!-- Список материалов -->
            <ul class="material-list">
              <li
                v-for="material in materials"
                :key="material.id"
                class="material-item"
              >
                <div v-if="editingLesson === lessonName" class="edit-material">
                  <input
                    v-model="editedMaterials[material.id]"
                    type="text"
                    class="material-name-input"
                  />
                </div>
                <span v-else>{{ material.name }}</span>
                <button
                  v-if="editingLesson === lessonName"
                  @click="deleteMaterial(material.id)"
                  class="delete-button"
                >
                  Удалить
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Вкладка: Домашние работы -->
      <div v-else class="homeworks-view">
        <div v-if="homeworks.length === 0" class="no-homeworks">
          Нет домашних работ для проверки
        </div>
        <div v-else class="homework-list">
          <div
            v-for="homework in homeworks"
            :key="homework.id"
            class="homework-item"
          >
            <div class="homework-info">
              <p><strong>ФИО:</strong> {{ homework.fio }}</p>
              <p><strong>Урок:</strong> {{ homework.lessonName }}</p>
              <p><strong>Материал:</strong> {{ homework.materialName }}</p>
            </div>

            <div class="buttons">
              <button @click="downloadFile(homework.file)">Скачать</button>
              <button @click="markAsChecked(homework.id)">проверено</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AddLessonModal from "../../components/AddLessonModal.vue";
import { ref, onMounted } from "vue";
import axios from "axios";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

// === Переменные ===
const loading = ref(true);
const homeworks = ref<
  {
    id: number;
    fio: string;
    lessonName: string;
    materialName: string;
    file: string;
    checked: boolean;
  }[]
>([]);
const courseId = Number(useRoute().params.courseId);
const courseName = ref("");
const chooseHomework = ref(false);
const editingLesson = ref<string | null>(null);
const editedLessonName = ref("");
const editedMaterials = ref<{ [materialId: number]: string }>({});
const addLessonModal = ref();

const addMaterialModal = ref();

const openAddMaterialModal = () => {
  addMaterialModal.value.openModal();
};

const onMaterialCreated = (lessonName: string, material: any) => {
  // Добавляем новый материал к соответствующему уроку
  if (!course.value[lessonName]) {
    course.value[lessonName] = [];
  }
  course.value[lessonName].push({
    id: material.id,
    name: material.name,
    type: material.type,
  });
};

// Данные курса
const course = ref<{
  [lessonName: string]: {
    id: number;
    name: string;
    type: string;
  }[];
}>({});

const openAddLessonModal = () => {
  addLessonModal.value.openModal();
};

const onLessonCreated = (lessonName: string) => {
  course.value[lessonName] = [];
  alert(`Урок "${lessonName}" успешно создан`);
  // здесь можно обновить интерфейс
};

// === Получение данных курса ===
const getCourseDetails = async () => {
  try {
    const response = await axios.post(`${apiBase}/api/getCourseForTeacher`, {
      courseId,
    });
    courseName.value = response.data.course.name;
    course.value = response.data.course;
  } catch (error) {
    console.error("Ошибка при получении данных курса:", error);
  } finally {
    loading.value = false;
  }
};

// === Получение домашних работ ===
const getHomeworks = async () => {
  try {
    const response = await axios.post(`${apiBase}/api/homework`, { courseId });
    homeworks.value = response.data.homeworks;
  } catch (error) {
    console.error("Ошибка при получении домашних работ:", error);
  }
};

// === Обработчики событий ===

// Скачивание файла
const downloadFile = async (fileUrl: string) => {
  const response = await fetch(`${apiBase}/api/download`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ path: fileUrl }),
  });

  if (!response.ok) {
    throw new Error("Ошибка при получении файла");
  }

  const blob = await response.blob();
  let tmp = fileUrl.split("/");
  const fileName = tmp[tmp.length - 1];
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
};

// Пометить домашнюю работу как проверенную
const markAsChecked = async (homeworkId: number) => {
  const response = await axios.post(`${apiBase}/api/homework/checked`, {
    userProgressId: homeworkId,
  });
  if (response.status === 200) {
    homeworks.value = homeworks.value.filter((h) => h.id !== homeworkId);
  }
};

// Редактирование урока — активация
const editLesson = (lessonName: string) => {
  if (editingLesson.value === lessonName) {
    editingLesson.value = null;
  } else {
    editingLesson.value = lessonName;
    editedLessonName.value = lessonName;

    // Инициализируем редактирование названий материалов
    const materials = course.value[lessonName];
    const temp: { [materialId: number]: string } = {};
    materials.forEach((m) => {
      temp[m.id] = m.name;
    });
    editedMaterials.value = temp;
  }
};

// Сохранение изменённого названия урока
const saveLesson = async (originalLessonName: string) => {
  try {
    const newLessonName = editedLessonName.value.trim();

    // --- Локальное обновление ---
    const updatedCourse = { ...course.value };

    // Обновляем названия материалов локально
    updatedCourse[originalLessonName].forEach((m) => {
      m.name = editedMaterials.value[m.id] || m.name;
    });

    // Переименовываем урок локально (если нужно)
    if (newLessonName && newLessonName !== originalLessonName) {
      updatedCourse[newLessonName] = updatedCourse[originalLessonName];
      delete updatedCourse[originalLessonName];
    }

    course.value = updatedCourse;
    editingLesson.value = null;

    // --- Запросы на сервер ---

    // 1. Обновление названий материалов
    for (const material of course.value[newLessonName || originalLessonName]) {
      await axios.post(`${apiBase}/api/updateMaterial`, {
        materialId: material.id,
        newName: material.name,
      });
    }

    // 2. Переименование урока (если было изменено)
    if (newLessonName && newLessonName !== originalLessonName) {
      await axios.post(`${apiBase}/api/updateLesson`, {
        courseId: courseId,
        oldName: originalLessonName,
        newName: newLessonName,
      });
    }
  } catch (error) {
    console.error("Ошибка при сохранении урока:", error);
    alert("Не удалось сохранить изменения на сервере");
  }
};

// Удаление урока
const removeLesson = (lessonName: string) => {
  const updatedCourse = { ...course.value };
  delete updatedCourse[lessonName];
  course.value = updatedCourse;
};

// Удаление материала
const deleteMaterial = async (materialId: number) => {
  try {
    await axios.post(`${apiBase}/api/deleteMaterial`, { materialId });

    for (let lesson in course.value) {
      course.value[lesson] = course.value[lesson].filter(
        (m: any) => m.id !== materialId
      );
    }
  } catch (error) {
    console.error("Ошибка при удалении материала:", error);
  }
};

// === Инициализация ===
onMounted(async () => {
  await getCourseDetails();
  await getHomeworks();
});
</script>

<style scoped>
.bizlab-logo {
  margin-left: 5%;
  margin-top: 2%;
}

.course-page {
  max-width: 800px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}

.edit-material {
  display: flex;
  align-items: center;
  gap: 10px;
}

.material-name-input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  flex-grow: 1;
  width: 100%;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ccc;
}

.header img {
  width: 150px;
}

.header h1 {
  font-size: 24px;
  margin: 0;
}

.header nav button {
  background-color: #ff7f50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
  margin-left: 10px;
}

.header nav .active {
  background-color: #2c3e50;
}

.actions {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.create-lesson {
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
}

.upload-material {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 5px;
  cursor: pointer;
}

.lessons-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.lesson-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.lesson-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.edit-mode {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-grow: 1;
}

.lesson-name-input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  flex-grow: 1;
}

.lesson-actions {
  display: flex;
  gap: 8px;
}

.edit-button,
.save-button,
.delete-button {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.material-list {
  list-style-type: none;
  padding: 0;
}

.material-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.material-item span {
  flex-grow: 1;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.buttons button {
  padding: 8px 16px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.no-homeworks {
  text-align: center;
  font-size: 18px;
  margin-top: 50px;
}
</style>
