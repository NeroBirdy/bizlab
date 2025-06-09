<template>
  <Backimages :variable="2" />
  <BizlabLogo />
  <DeleteModal ref="deleteElementRef" :course="course" :elementId="elementId" :type="type" :toDelete="toDelete" />

  <div v-if="showModal" class="modal-overlay">
    <div class="modal">
      <h1 class="h1-modal">Вы уверены что хотите отметить данную работу?</h1>
      <div class="modal-buttons">
        <button class="btn" @click="closeModal">Нет</button>
        <button class="btn" @click="markAsChecked(tempWorkId)">Да</button>
      </div>
    </div>
  </div>

  <div class="course-page">
    <header class="header flex-col flex items-center justify-center mr-auto ml-auto">
      <h1>Курс {{ courseName }}</h1>
      <nav class="nav-buttons">
        <button @click="chooseHomework = false" :class="{ active: !chooseHomework }">
          Учебные материалы
        </button>
        <button @click="chooseHomework = true" :class="{ active: chooseHomework }">
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
          <AddLessonModal ref="addLessonModal" :courseId="courseId" @lesson-created="onLessonCreated" />
          <button class="upload-material" @click="openAddMaterialModal">
            Загрузить материал
          </button>

          <!-- Подключение модала -->
          <AddMaterialModal ref="addMaterialModal" :course="course" :courseId="courseId"
            @material-created="onMaterialCreated" />
          <button class="add-prepod" @click="openUserModal(courseId)">
            Добавить преподавателя
          </button>
          <AddUserOnCourse :role="1" ref="addUserModalRef" />

        </div>
        <!-- Список уроков -->
        <div v-if="course" class="lessons-container">
          <div v-for="(lesson, lessonId, index) in course" :key="lessonId" class="lesson-card">
            <div class="lesson-header">
              <!-- Режим редактирования -->
              <div v-if="editingLesson === lessonId" class="edit-mode">
                <input v-model="editedLessonName" type="text" placeholder="Название урока" class="lesson-name-input" />
                <button @click="saveLesson(lessonId)" class="save-button btn">
                  Сохранить
                </button>
              </div>

              <!-- Обычный режим -->
              <div v-else class="lesson-text">
                <span>Урок {{ index + 1 }} {{ lesson.name }}</span>
                <p class="text-black">
                  {{ Object.keys(lesson.materials).length }} материала
                </p>
              </div>

              <!-- Кнопки управления -->
              <div class="lesson-actions">
                <button v-if="editingLesson !== lessonId" @click="editLesson(lessonId)" class="edit-button btn">
                  Редактировать
                </button>
                <button v-if="editingLesson === lessonId" @click="deleteElement(lessonId, NaN, 2)"
                  class="delete-button btn">
                  удалить
                </button>
              </div>
            </div>

            <!-- Список материалов -->
            <ul v-if="editingLesson && editingLesson === lessonId" class="material-list">
              <li v-for="material in lesson.materials" :key="material.id" class="material-item">
                <div v-if="editingLesson === lessonId" class="edit-material">
                  <input v-model="editedMaterials[material.id]" type="text" class="material-name-input" />
                </div>
                <span v-else>{{ material.name }}</span>
                <button v-if="editingLesson === lessonId" @click="deleteElement(material.id, lessonId, 0)"
                  @element-deleted="handleChanges" class="delete-button btn">
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
        <div v-else class="homework-list flex">
          <div v-for="homework in homeworks" :key="homework.id" class="homework-item">
            <div class="homework-info">
              <p class="name"><strong>ФИО:</strong> {{ homework.fio }}</p>
              <p class="info-item">
                <strong>Урок:</strong>
                {{ homework.lessonName }}
              </p>
              <p class="info-item">
                <strong>Материал:</strong>
                {{ homework.materialName }}
              </p>
            </div>

            <div class="buttons">
              <button @click="downloadFile(homework.file)" class="btn bg-[#3840A9]">
                Скачать
              </button>
              <button @click="openModal(homework.id)" class="btn bg-[#328862]">
                проверено
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="flex justify-center">
    <button class="btn delete-button" @click="deleteElement(courseId, 1, 1)">
      Удалить курс
    </button>
  </div>
</template>

<script setup lang="ts">
import AddLessonModal from "../../components/AddLessonModal.vue";
import DeleteModal from "../../components/deleteModal.vue";
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
const editingLesson = ref<number | null>(null);
const editedLessonName = ref("");
const editedMaterials = ref<{ [materialId: number]: string }>({});
const addLessonModal = ref();
const deleteElementRef = ref();
const elementId = ref();
const type = ref();
const toDelete = ref();
const tempWorkId = ref();
const showModal = ref(false);
const addUserModalRef = ref();

const addMaterialModal = ref();

const openAddMaterialModal = () => {
  addMaterialModal.value.openModal();
};

const openAddLessonModal = () => {
  addLessonModal.value.openModal();
};

function openModal(id) {
  tempWorkId.value = id;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
  tempWorkId.value = null;
}

const onMaterialCreated = (lessonId: number, material: any) => {
  course.value[lessonId].materials.push({
    id: material.id,
    name: material.name,
    type: material.type,
  });
};

// Данные курса
const course = ref<{
  [lessonId: number]: {
    id: number;
    name: string;
    materials: {
      id: number;
      name: string;
      type: string;
    }[];
  };
}>({});

const openUserModal = (courseId: number) => {
  addUserModalRef.value?.openModal(courseId);
};

const handleChanges = (courseCopy: Object) => {
  // course.value = courseCopy;
};

const onLessonCreated = (lessonId: number, lessonName: string) => {
  course.value[lessonId] = { id: lessonId, name: lessonName, materials: [] };
  alert(`Урок "${lessonName}" успешно создан`);
};

// === Получение данных курса ===
const getCourseDetails = async () => {
  try {
    const response = await axios.post(`${apiBase}/api/getCourseForTeacher`, {
      courseId,
    });
    courseName.value = response.data.courseName;
    course.value = response.data.course;
    console.log(course.value);
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

const deleteElement = (elId: number, lessonId: number, tp: number) => {
  console.log(deleteElementRef.value.openModal());
  type.value = tp;
  if (tp == 0) {
    toDelete.value = "материал";
    elementId.value = { materialId: elId, lessonId: lessonId };
  } else if (tp == 2) {
    toDelete.value = "урок";
    elementId.value = { lessonId: elId, courseId: courseId };
  } else {
    toDelete.value = "курс";
    elementId.value = elId;
  }
  deleteElementRef.value.openModal();
};

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
  closeModal();
};

const editLesson = (lessonId: number) => {
  if (editingLesson.value === lessonId) {
    editingLesson.value = null;
  } else {
    editingLesson.value = lessonId;
    editedLessonName.value = course.value[lessonId].name;

    const materials = course.value[lessonId].materials;
    const temp: { [materialId: number]: string } = {};
    materials.forEach((m) => {
      temp[m.id] = m.name;
    });
    editedMaterials.value = temp;
  }
};

const saveLesson = async (lessonId: number) => {
  try {
    const newLessonName = editedLessonName.value.trim();

    const oldName = course.value[lessonId].name;
    const flag = Object.values(course.value).some((lesson) => {
      if (newLessonName == lesson.name && lessonId != lesson.id) {
        return true;
      }
      return false;
    });

    if (oldName != newLessonName && !flag) {
      course.value[lessonId].name = newLessonName;
    }

    editingLesson.value = null;

    for (const material of course.value[lessonId].materials) {
      if (editedMaterials.value[material.id] != material.name) {
        await axios.post(`${apiBase}/api/updateMaterial`, {
          materialId: material.id,
          newName: editedMaterials.value[material.id],
        });
        material.name = editedMaterials.value[material.id];
      }
    }

    if (newLessonName && newLessonName !== oldName) {
      await axios.post(`${apiBase}/api/updateLesson`, {
        courseId: courseId,
        oldName: oldName,
        newName: newLessonName,
      });
    }
  } catch (error) {
    console.error("Ошибка при сохранении урока:", error);
    alert("Не удалось сохранить изменения на сервере");
  }
};

onMounted(async () => {
  await getCourseDetails();
  await getHomeworks();
});
</script>

<style scoped>
.h1-modal {
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

.modal {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
  position: relative;
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

.lesson-text {
  font-family: "Inter";
  width: 100%;

  p,
  span {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  span {
    font-size: 24px;
  }

  p {
    font-size: 20px;
  }
}

.nav-buttons {
  width: 100%;
  display: flex;
  justify-content: space-between;

  button {
    font-family: "Uncage";
    font-size: 24px;
    color: #ff7f50;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;

    &:hover {
      text-decoration: underline;
    }
  }

  .active {
    background-color: #e25d35;
    border-radius: 20px;
    color: white;

    &:hover {
      text-decoration: none;
    }
  }
}

.course-page {
  background-color: rgb(236, 236, 236);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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

.loading {
  font-family: "Uncage";
  font-size: 24px;
  width: 100%;
  text-align: center;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #ccc;
  height: max-content;
}

.header img {
  width: 150px;
}

.header h1 {
  font-size: 24px;
  margin: 0;
}

.actions {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  justify-content: space-evenly;
  margin-top: 10px;
  .create-lesson,
  .upload-material,
  .add-prepod {
    font-family: "Uncage";
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.2s;
    &:hover {
      transform: translateY(-5px) scale(1.05);
      opacity: 70%;
    }
  }

  .create-lesson {
    background-color: #328862;
  }

  .upload-material {
    background-color: #3840a9;
  }

  .add-prepod {
    background-color: #f0ac02;
  }
}


.lesson-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;
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

.edit-button {
  background-color: var(--p-sky-600);
  font-size: 16px;
}

.delete-button {
  background-color: #e74c3c;
  font-size: 16px;
}

.save-button {
  background-color: #328862;
  font-size: 16px;
  margin-right: 5px;
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

.no-homeworks {
  text-align: center;
  font-size: 18px;
  font-family: "Uncage";
  margin-top: 50px;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.homework-item {
  margin-top: 10px;
  width: 100%;
  display: flex;
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 10px;

  .buttons {
    width: 20%;
  }

  .homework-info {
    width: 80%;
    font-family: "Inter";

    .name {
      font-size: 20px;
    }

    .info-item {
      font-size: 18px;
    }
  }
}

@media (max-width: 820px) {
  .course-page {
    margin: 20px;
  }

  .nav-buttons {
    button {
      font-size: 3vw;
    }
  }
}

@media (max-width: 580px) {
  .lesson-card {
    position: relative;

    .edit-button {
      display: none;
    }
  }

  .save-button {
    display: none;
  }

  .material-item {
    gap: 10px;
    justify-content: inherit;

    .edit-material {
      width: 100%;
    }
  }

  .mobile-edit-btn {
    display: flex;
    position: absolute;
    right: -10px;
    top: -5px;
  }

  .lesson-header {
    gap: 10px;
  }

  .actions {
    flex-direction: column;
    margin-bottom: 20px;
  }
}

@media (max-width: 500px) {
  .nav-buttons {
    button {
      font-size: 4vw;
    }
  }

  .hide-block {
    display: none;
  }

  .mobile-save-btn {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 40px;
    height: max-content;
  }

  .save-button,
  .delete-button {
    margin-left: 10px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .save-button {
    display: none;
  }

  .material-item {
    justify-content: start;
  }

  .save-button {
    margin-left: 0;
  }

  .homework-item {
    flex-direction: column;

    .buttons {
      margin-top: 10px;
      width: 100%;
    }

    .homework-info {
      text-align: center;
      width: 100%;
      strong {
        display: block;
      }
    }
  }
}

@media (max-width: 425px) {
  .nav-buttons {
    flex-direction: column;
    gap: 10px;
    margin-top: 10px;
  }

  .lesson-text {
    span,
    p {
      align-items: start;
    }
  }

  .lesson-header,
  .material-item {
    gap: 0;
  }
  .lesson-name-input {
    width: 100%;
  }
}

@media (max-width: 385px) {
}

@media (max-width: 375px) {
  .nav-buttons {
    button {
      font-size: 5vw;
    }
  }
}

@media (max-width: 320px) {
  .course-page {
    margin: 20px 0;
  }
}

</style>
