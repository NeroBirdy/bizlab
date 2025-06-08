<template>
  <Backimages :variable="2" />
  <BizlabLogo />
  <div class="student-course-page">
    <!-- Шапка -->
    <header class="header">
      <h1>Курс {{ courseName }}</h1>
    </header>

    <!-- Основной контент -->
    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else>
      <!-- Список уроков -->
      <div
        v-for="(materials, lessonName, index) in course"
        :key="lessonName"
        class="lesson-card"
      >
        <h2>Урок {{ index + 1 }} {{ lessonName }}</h2>

        <!-- Материалы -->
        <ul class="material-list">
          <li
            v-for="material in materials"
            :key="material.id"
            class="material-item"
          >
            <span>{{ material.name }}</span>

            <div v-if="['1', '2'].includes(material.type)" class="flex gap-4">
              <button
                v-if="!done.includes(material.id)"
                @click="downloadFile(material.file)"
                class="bg-[#3840A9] btn"
              >
                Скачать
              </button>
              <input
                v-if="!done.includes(material.id)"
                type="file"
                :id="'fileInput-' + material.id"
                @change="handleFileUpload($event, material)"
                style="display: none"
              />
              <label
                v-if="!done.includes(material.id) && material.type == 2"
                :for="'fileInput-' + material.id"
                class="bg-[#F0AC02] btn block"
              >
                Прикрепить
              </label>
              <h2 v-if="done.includes(material.id)">Выполнено</h2>
            </div>

            <a
              v-else-if="material.type == 4 && !done.includes(material.id)"
              :href="material.link"
              target="_blank"
              rel="noopener noreferrer"
              class="bg-[#3840A9] btn"
              >Перейти по ссылке</a
            >
            <h2 v-else-if="material.type == 3 && done.includes(material.id)">
              Выполнено
            </h2>
            <a
              v-else-if="material.type == 3 && !done.includes(material.id)"
              :href="material.link"
              target="_blank"
              class="bg-[#3840A9] btn"
              @click="navigateTo(`/test/${material.id}`)"
            >
              Перейти к тесту
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

// === Переменные ===

const loading = ref(true);
const userId = ref<number | null>(null);
const done = ref([]);
const courseName = ref("");
const course = ref<{
  [lessonName: string]: Array<{
    id: number;
    name: string;
    type: number;
    file?: string;
    link?: string;
  }>;
}>();

const uploadedFiles = ref<{ [materialId: number]: string }>({});

const getDone = async () => {
  const response = await axios.post(`${apiBase}/api/getDone`, {
    userId: userId.value,
  });

  done.value = response.data.materials;
};

const handleFileUpload = async (event: Event, material: any) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  try {
    const formData = new FormData();
    formData.append("userId", userId.value!.toString());
    formData.append("materialId", material.id.toString());
    formData.append("file", file);

    // Отправка на сервер
    const response = await axios.post(`${apiBase}/api/upload`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    alert("Файл успешно загружен!");

    // Сохраняем имя загруженного файла
    uploadedFiles.value[material.id] = file.name;
  } catch (error) {
    console.error("Ошибка при загрузке домашней работы:", error);
    alert("Не удалось загрузить файл");
  }

  // Очистка поля ввода, чтобы можно было повторно загрузить тот же файл
  target.value = "";
};

// === Получение данных курса для студента ===
const getCourseDetails = async () => {
  const token = useCookie("auth_token").value;

  if (!token) {
    console.error("Токен отсутствует");
    loading.value = false;
    return;
  }

  try {
    const decodedToken = jwtDecode(token);
    userId.value = decodedToken.user_id || null; // Предполагается, что ID студента хранится в cookie
    const courseId = Number(useRoute().params.courseId);

    const response = await axios.get(`${apiBase}/api/getCourseForUser`, {
      params: {
        userId: userId.value,
        courseId: courseId,
      },
    });
    console.log(response.data);
    courseName.value = response.data.courseName;
    console.log(courseName);
    course.value = response.data.course;
  } catch (error) {
    console.error("Ошибка при получении данных курса:", error);
  } finally {
    loading.value = false;
  }
};

// === Скачивание файла ===
const downloadFile = async (fileUrl: string) => {
  try {
    const response = await axios.post(
      `${apiBase}/api/download`,
      {
        path: fileUrl,
      },
      {
        responseType: "blob",
      }
    );

    const blob = new Blob([response.data], {
      type: response.headers["content-type"],
    });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = fileUrl.split("/").pop() || "file";
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Ошибка при скачивании файла:", error);
    alert("Не удалось скачать файл");
  }
};

// === Инициализация ===
onMounted(async () => {
  await getCourseDetails();
  await getDone();
});
</script>

<style scoped>
.student-course-page {
  background-color: rgb(236, 236, 236);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}

.btn {
  font-family: "Uncage";
  font-size: 18px;
  color: white;
  border: none;
  padding: 5px 15px;
  border-radius: 25px;
  height: max-content;
  cursor: pointer;

  transition: all 0.2s;
  &:hover {
    transform: translateY(-5px) scale(1.05);
    opacity: 70%;
  }
}

.loading {
  font-family: "Uncage";
  font-size: 24px;
  width: 100%;
  text-align: center;
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
}

.header h1 {
  font-family: "Uncage";
  font-size: 24px;
  margin: 0;
  padding: 0;
}

.lesson-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;

  h2 {
    font-family: "Inter";
    font-size: 24px;
    border-bottom: 1px solid #ccc;
    margin-bottom: 10px;
  }
}

.material-list {
  margin-left: auto;
  margin-right: auto;
  width: 100%;
  list-style-type: none;
  padding: 0;
}

.material-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px 5%;
  border-radius: 5px;
  background-color: rgb(236, 236, 236);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.301);
  span {
    font-family: "Inter";
    font-size: 20px;
  }
}

.download-button {
  padding: 5px 10px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.test-link {
  padding: 5px 10px;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
}
</style>
