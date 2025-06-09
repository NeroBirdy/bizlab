<template>
  <Backimages :variable="2" />
  <div class="logout">
    <p class="logout-btn" @click="logout">ВЫЙТИ ИЗ ЛИЧНОГО КАБИНЕТА</p>
    <a v-if="role == 2" class="logout-btn admin" href="/admin">Админка</a>
  </div>

  <BizlabLogo />
  <div v-if="role == 1 || role == 2" class="teacher-courses">
    <div class="flex gap-10 mb-10">
      <h1 class="teacher-link text-[#3840a9] items-center text-center flex">
        Мои курсы
      </h1>
      <button
        @click="navigateTo('/createCourse')"
        class="teacher-link btn create-btn"
      >
        Создать курс
      </button>
      <button
        @click="openStudentRegistrationModal"
        class="teacher-link btn student-btn"
      >
        Зарегистрировать студента
      </button>
    </div>

    <AddStudentModal ref="addStudentModalRef" />
    <!-- Список курсов -->
    <div v-if="courses.length > 0" class="courses-list" id="courses-list">
      <div
        v-for="(course, index) in courses"
        :key="course.id"
        class="course-card"
      >
        <div class="flex">
          <img
            :src="course.picture"
            alt="Картинка курса"
            class="course-image"
            @click="navigateTo(`/course/${course.id}`)"
          />
          <div class="card-buttons">
            <p class="text-center">
              Ожидают проверки {{ course.needToCheck }} работ
            </p>
            <div class="flex justify-center">
              <button @click="openUserModal(course.id)" class="btn course-btn">
                Зачислить ученика
              </button>
            </div>
          </div>
        </div>

        <!-- Название курса -->
        <div class="course-info">
          <h3 style="cursor: pointer">
            Курс {{ index + 1 }}: {{ course.name }}
          </h3>
        </div>
      </div>
    </div>

    <!-- Сообщение при отсутствии курсов -->
    <p v-else class="no-courses">
      {{ loading ? "Загрузка..." : "Нет доступных курсов" }}
    </p>

    <!-- Модальное окно -->
    <AddUserOnCourse ref="addUserModalRef" />
  </div>
  <div v-if="role == 0" class="teacher-courses">
    <div class="header flex">
      <div class="logo flex">
        <h1 class="teacher-link text-[#3840a9] items-center text-center flex">
          МОИ КУРСЫ
        </h1>
      </div>
    </div>

    <div
      v-if="coursesForStudent.length > 0"
      v-for="(course, index) in coursesForStudent"
      class="courses-list"
    >
      <div
        @click="navigateTo(`/courseForStudent/${course.id}`)"
        class="course-card mb-10"
      >
        <div class="flex items-center">
          <div class="image">
            <img
              :src="course.picture"
              alt="Картинка курса"
              class="course-image"
            />
          </div>
          <div class="course-bar">
            <h1>ТЕКУЩИЙ ПРОГРЕСС КУРСА</h1>
            <ProgressBar
              :show-value="false"
              :value="course.progress"
            ></ProgressBar>
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

const addStudentModalRef = ref();
const courses = ref([]);
const userId = ref<number | null>(null);
const loading = ref(true);
const role = ref();
const coursesForStudent = ref();
const userStore = useAuthStore();
const addUserModalRef = ref();

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
.p-progressbar {
  background: #3288624a !important;
}

.background-vectors {
  z-index: -1;
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

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

  padding: 10px 20px;
}
</style>
