<template>
  <div class="logout">
    <p class="logout-btn" @click="logout">ВЫЙТИ ИЗ ЛИЧНОГО КАБИНЕТА</p>
    <a v-if="role == 2" class="logout-btn admin" href="/admin">Админка</a>
  </div>

  <BizlabLogo />
  <div class="bg-template">
    <Backimages />
  </div>

  <div v-if="role == 1 || role == 2" class="teacher-courses">
    <div class="teacher-header">
      <h1 class="teacher-link text-[#3840a9] items-center text-center flex">
        Мои курсы
      </h1>
      <button @click="navigateTo('/createCourse')" class="teacher-link btn create-btn">
        Создать курс
      </button>
      <button @click="openStudentRegistrationModal" class="teacher-link btn student-btn">
        Зарегистрировать студента
      </button>
    </div>

    <AddStudentModal ref="addStudentModalRef" />
    <!-- Список курсов -->
    <div v-if="courses.length > 0" class="courses-list" id="courses-list">
      <div v-for="(course, index) in courses" :key="course.id" class="course-card">
        <div class="card-container">
          <img :src="course.picture" alt="Картинка курса" class="course-image"
            @click="navigateTo(`/course/${course.id}`)" />
          <div class="card-buttons">
            <p class="text-center" @click="navigateTo(`/course/${course.id}`)">
              Ожидают проверки {{ course.needToCheck }} работ
            </p>
            <div class="flex justify-center">
              <button @click="openDialog.show; courseId = course.id" class="btn course-btn">
                Добавить пользователя
              </button>
              <Popover ref="openDialog">
                <div class="flex flex-col gap-4">
                  <button class="btn course-btn" @click="openUserModal(courseId); roleForAdd = 0">
                    Удалить ученика
                  </button>
                  <button class="btn course-btn" @click="openUserModal(courseId); roleForAdd = 1">
                    Удалить учителя
                  </button>
                </div>
              </Popover>
            </div>
          </div>
        </div>

        <!-- Название курса -->
        <div class="course-info">
          <h3 style="cursor: pointer">
            Курс {{ index + 1 }}: {{ course.name }}
          </h3>
          <button @click="openDialog.show; courseId = course.id" class="btn course-btn adaptive-btn">
            Добавить пользователя
          </button>
          <Popover ref="openDialog">
            <div class="flex flex-col gap-4">
              <button class="btn course-btn" @click="openUserModal(courseId); roleForAdd = 0">
                Удалить ученика
              </button>
              <button class="btn course-btn" @click="openUserModal(courseId); roleForAdd = 1">
                Удалить учителя
              </button>
            </div>
          </Popover>
        </div>
      </div>
    </div>

    <p v-else class="no-courses">
      {{ loading ? "Загрузка..." : "Нет доступных курсов" }}
    </p>
    <AddUserOnCourse :role="roleForAdd" :action="0" ref="addUserModalRef" />
  </div>
  <div v-if="role == 0" class="teacher-courses">
    <div class="header flex">
      <div class="logo flex">
        <h1 class="teacher-link text-[#3840a9] items-center text-center flex">
          МОИ КУРСЫ
        </h1>
      </div>
    </div>

    <div v-if="coursesForStudent.length > 0" v-for="(course, index) in coursesForStudent" class="courses-list">
      <div @click="navigateTo(`/courseForStudent/${course.id}`)" class="course-card mb-10">
        <div class="card-container-student">
          <div class="image">
            <img :src="course.picture" alt="Картинка курса" class="course-image" />
          </div>
          <div class="course-bar">
            <h1>ТЕКУЩИЙ ПРОГРЕСС КУРСА</h1>
            <ProgressBar :show-value="false" :value="course.progress"></ProgressBar>
            <p>{{ parseInt(course.progress) }} %</p>
          </div>
        </div>
        <div class="course-info">
          <h3 style="cursor: pointer">
            Курс {{ index + 1 }}: {{ course.name }}
          </h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import AddStudentModal from "../../components/AddStudent.vue";
import ProgressBar from "primevue/progressbar";
import Popover from 'primevue/popover';

const addStudentModalRef = ref();
const courses = ref([]);
const userId = ref<number | null>(null);
const loading = ref(true);
const role = ref();
const coursesForStudent = ref();
const userStore = useAuthStore();
const addUserModalRef = ref();
const roleForAdd = ref();
const openDialog = ref();
const courseId = ref();

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

const openStudentRegistrationModal = () => {
  addStudentModalRef.value?.openModal();
};

const logout = async () => {
  //   const response = await axios.post(`${apiBase}/api/auth/logout`);
  userStore.logoutUser();
  navigateTo("/");
};

const getCoursesByUser = async () => {
  const response = await axios.post(`${apiBase}/api/getCourseByUser`, {
    userId: userId.value,
  });

  coursesForStudent.value = response.data.courses;
};

const fetchUserData = async () => {
  const token = useCookie("auth_token").value;

  if (!token) {
    console.error("Токен отсутствует");
    loading.value = false;
    return;
  }

  try {
    const decodedToken = jwtDecode(token);
    userId.value = decodedToken.user_id || null;

    const response = await axios.post(`${apiBase}/api/getUser`, {
      userId: userId.value,
    });

    role.value = response.data.role;
    if (role.value == 0) {
      getCoursesByUser();
    }
  } catch (error) {
    console.error("Ошибка при декодировании токена:", error);
  }
};

const getTeacherCourses = async () => {
  if (!userId.value) {
    console.warn("Не удалось получить ID пользователя");
    loading.value = false;
    return;
  }

  try {
    const response = await axios.get(
      `${apiBase}/api/getCoursesForTeacher?teacherId=${userId.value}`
    );
    courses.value = response.data.courses || [];
  } catch (error) {
    console.error("Ошибка при загрузке курсов:", error);
    alert("Не удалось загрузить курсы. Попробуйте позже.");
  } finally {
    loading.value = false;
  }
};

const openUserModal = (courseId: number) => {
  addUserModalRef.value?.openModal(courseId);
};

onMounted(async () => {
  await fetchUserData();
  await getTeacherCourses();
});
</script>

<style lang="scss" scoped>
.teacher-link {
  font-size: 24px;
  text-transform: uppercase;
  font-family: "Uncage";
}

.create-btn {
  background-color: #f0ac02;
  border-radius: 25px;
}

.student-btn {
  background-color: #328862;
  border-radius: 25px;
}

.btn {
  transition: all 0.2s;
  color: white;
  padding: 5px 20px;

  &:hover {
    transform: translateY(-10px);
    opacity: 0.8;
  }
}

.teacher-courses {
  max-width: 1000px;
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.bg-template {
  width: 100vw;
}

.card-buttons {
  @apply flex gap-10 flex-col w-full justify-center items-center;
  font-size: 24px;
  font-family: "Uncage";

  p {
    color: #e25d35;
  }
}

.logout {
  position: absolute;
  top: 2%;
  right: 2%;
}

.logout-btn {
  cursor: pointer;
  width: 100px;
  font-family: "Uncage";
  color: #e15d34;
  transition: all 0.5s;

  &:hover {
    transform: translateX(-10px);
  }
}

.teacher-header {
  @apply flex gap-10 mb-10;
}

.admin {
  color: var(--p-cyan-400);
  display: block;
}

.courses-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.image {
  width: 50%;
}

.header {
  justify-content: space-between;
}

.course-card {
  background-color: rgb(223, 235, 247);
  width: 100% !important;
  padding: 15px 30px;
  border-radius: 5px;
  transition: transform 0.2s ease-in-out;
  width: calc(50% - 10px);
  cursor: pointer;
}

.course-image {
  height: 250px;
  max-width: 400px;
  min-width: 400px;
  object-fit: cover;
  margin-bottom: 10px;
  border-radius: 15px;
}

.adaptive-btn {
  display: none;
}

.course-info {
  width: 100%;
  font-size: 30px;
  align-items: center;
  justify-content: center;
  color: #3840a9;
  font-family: "Uncage";
}

.course-bar {
  width: 50%;
  height: max-content;
  font-size: 30px;
  align-items: center;
  justify-content: center;
  color: #3840a9;
  font-family: "Uncage";
}

.no-courses {
  text-align: center;
  font-size: 18px;
  color: #666;
}

.course-btn {
  background-color: #3840a9;
  border-radius: 20px;
  color: white;
  z-index: 10;
  padding: 10px 20px;
}

.card-container {
  display: flex;
}

.card-container-student {
  display: flex;
  align-items: center;
}

@media (max-width: 1040px) {
  .teacher-courses {
    margin: 20px 20px;
  }
}

@media (max-width: 1070px) {
  .logout {
    display: flex;
    flex-direction: row-reverse;
  }
}

@media (max-width: 1024px) {
  .teacher-courses {
    max-width: auto;
    margin: 20px 20px;
  }

  .course-image {
    max-width: 40vw;
    min-width: 40vw;
  }

  .image {
    width: max-content;
    margin-right: 10px;
  }

  .teacher-header {
    @apply justify-center;
  }

  .btn {
    font-size: 2.4vw;
  }
}

@media (max-width: 768px) {
  .teacher-courses {
    max-width: auto;
    margin: 20px 50px;
  }

  .image {
    margin-right: 0;
  }

  .course-card {
    display: flex;
    flex-direction: column-reverse;
    padding: 15px 10px;
    position: relative;
  }

  .card-container-student {
    display: flex;
    justify-content: center;
    position: relative;
    width: max-content;
    margin-left: auto;
    margin-right: auto;
  }

  .course-image {
    max-width: 70vw;
    min-width: 70vw;
  }

  .course-bar {
    width: 100%;
    padding: 10px 20px;
    background-color: #edefffa6;
    border-radius: 15px;
    position: absolute;
    bottom: 0;

    h1 {
      font-size: 16px;
    }
  }

  .card-container {
    margin-top: 20px;
    flex-direction: column-reverse;
    position: relative;
    justify-content: center;
    align-items: center;
    width: max-content;
    margin-left: auto;
    margin-right: auto;

    .course-image {
      margin: 0;
    }
  }

  .card-buttons {
    flex-direction: column-reverse;
    gap: 10px;
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: rgba(175, 175, 175, 0.507);
    border-radius: 15px;

    .course-btn {
      display: none;
    }

    p {
      width: max-content;
      font-size: 4vw;
    }
  }

  .adaptive-btn {
    display: block;
  }

  .course-info {
    display: flex;
    justify-content: space-around;

    h3 {
      font-size: 4vw;
    }
  }
}

@media (max-width: 560px) {
  .teacher-header {
    flex-direction: column;
    gap: 2vw;
    margin-top: 20px;

    .btn {
      font-size: 20px;
    }
  }
}

@media (max-width: 425px) {
  .teacher-header {
    h1 {
      margin-bottom: 20px;
    }
  }

  .teacher-courses {
    max-width: auto;
    margin: 20px 10px;
  }

  .course-image {
    max-width: 90vw;
    min-width: 90vw;
  }

  .logout {
    flex-direction: column;
  }

  .course-info {
    h3 {
      font-size: 5vw;
      text-align: center;
    }

    .btn {
      font-size: 4vw;
    }
  }
}

@media (max-width: 375px) {
  .course-card {
    padding: 0;
  }

  .card-container {
    margin-bottom: 10px;
  }

  .course-info {
    padding: 10px;
  }
}
</style>
