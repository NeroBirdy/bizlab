<template>
    <div v-if="role == 1" class="teacher-courses">
        <h2>МОИ КУРСЫ</h2>
        <button @click="navigateTo('/createCourse')">Создать курс</button>
        <button @click="openStudentRegistrationModal">Зарегистрировать студента</button>
        <AddStudentModal ref="addStudentModalRef" />
        <!-- Список курсов -->
        <div v-if="courses.length > 0" class="courses-list" id="courses-list">
            <div v-for="course in courses" :key="course.id" class="course-card">
                <!-- Картинка курса -->
                <img :src="course.picture" alt="Картинка курса" class="course-image"
                    @click="navigateTo(`/course/${course.id}`)" />

                <!-- Название курса -->
                <div class="course-info">
                    <h3 style="cursor: pointer;">{{ course.name }}</h3>
                    <p>Ожидают проверки {{ course.needToCheck }} работ</p>
                    <button @click="openUserModal(course.id)" class="btn">Зачислить ученика</button>
                </div>
            </div>
        </div>

        <!-- Сообщение при отсутствии курсов -->
        <p v-else class="no-courses">{{ loading ? 'Загрузка...' : 'Нет доступных курсов' }}</p>

        <!-- Модальное окно -->
        <AddUserOnCourse ref="addUserModalRef" />
    </div>
    <div v-if="role == 0">
        <div class="header flex">
            <div class="logo flex">
                <img class="logo h-10 mt-3 ml-5" src="/assets/images/bizlap-logo.svg" alt="bizlab" />
                <h1 class="ml-20 mt-10">МОИ КУРСЫ</h1>
            </div>
            <p class="logout" @click="logout">ВЫЙТИ ИЗ ЛИЧНОГО КАБИНЕТА</p>
        </div>


        <div v-if="coursesForStudent.length > 0" v-for="(course, index) in coursesForStudent" class="courses-list">
            <div @click="navigateTo(`/courseForStudent/${course.id}`)" class="course-card">
                <div class="image">
                    <img :src="course.picture" alt="Картинка курса" class="course-image" />
                    <h3 style="cursor: pointer;">Курс {{ index + 1 }}</h3>
                    <h3 style="cursor: pointer;">{{ course.name }}</h3>
                </div>
                <div class="course-info">
                    <h1>ТЕКУЩИЙ ПРОГРЕСС КУРСА</h1>
                    <ProgressBar :show-value=false :value="course.progress"></ProgressBar>
                    <p> {{ parseInt(course.progress) }} %</p>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { jwtDecode } from 'jwt-decode'
import AddStudentModal from '../../components/AddStudent.vue'
import ProgressBar from 'primevue/progressbar';


// === Переменные ===
const addStudentModalRef = ref()
const courses = ref([])
const userId = ref<number | null>(null)
const loading = ref(true)
const role = ref()
const coursesForStudent = ref()

// === Подключение модального окна ===
const addUserModalRef = ref()

// === Получение данных пользователя из токена ===
const config = useRuntimeConfig()
const apiBase = config.public.apiBase as string

// === Обработчик клика по кнопке "Зарегистрировать студента" ===
const openStudentRegistrationModal = () => {
    addStudentModalRef.value?.openModal()
};

const logout = async () => {
    const response = await axios.post(`${apiBase}/api/auth/logout`);
    navigateTo('/');
};

const getCoursesByUser = async () => {
    const response = await axios.post(`${apiBase}/api/getCourseByUser`, { 'userId': userId.value })

    coursesForStudent.value = response.data.courses
};

const fetchUserData = async () => {
    const token = useCookie('auth_token').value

    if (!token) {
        console.error('Токен отсутствует')
        loading.value = false
        return
    }

    try {
        const decodedToken = jwtDecode(token)
        userId.value = decodedToken.user_id || null

        const response = await axios.post(`${apiBase}/api/getUser`, { 'userId': userId.value })

        role.value = response.data.role
        if (role.value == 0) {
            getCoursesByUser()
        }

    } catch (error) {
        console.error('Ошибка при декодировании токена:', error)
    }
}

// === Загрузка курсов учителя ===
const getTeacherCourses = async () => {
    if (!userId.value) {
        console.warn('Не удалось получить ID пользователя')
        loading.value = false
        return
    }

    try {
        const response = await axios.get(`${apiBase}/api/getCoursesForTeacher?teacherId=${userId.value}`)
        courses.value = response.data.courses || []
    } catch (error) {
        console.error('Ошибка при загрузке курсов:', error)
        alert('Не удалось загрузить курсы. Попробуйте позже.')
    } finally {
        loading.value = false
    }
}

// === Обработчик клика по курсу ===
const openUserModal = (courseId: number) => {
    addUserModalRef.value?.openModal(courseId)
}

// === Инициализация ===
onMounted(async () => {
    await fetchUserData()
    await getTeacherCourses()
})
</script>

<style lang="scss" scoped>
.teacher-courses {
    max-width: 800px;
    margin: 20px auto;
}

.logout{
    display: flex;
    width: 100px;
    color: #E15D34;
}

.courses-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}
.image {
    width: 30%;
}

.header {
    justify-content: space-between;
}

.course-card {
    width: 65% !important;
    margin-left: auto;
    margin-right: auto;
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 10px;
    border-radius: 5px;
    transition: transform 0.2s ease-in-out;
    width: calc(50% - 10px);
    cursor: pointer;
    background-color: #fff;
}

.course-image {
    height: 170px;
    object-fit: cover;
    margin-bottom: 10px;

    border-radius: 15px;
}

.course-info {
    width: 65%;
    font-size: 30px;
    text-align: center;
    margin-left: auto;
    margin-right: auto;
    align-items: center;
    justify-content: center;
}

.no-courses {
    text-align: center;
    font-size: 18px;
    color: #666;
}
</style>