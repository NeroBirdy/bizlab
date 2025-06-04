<template>
    <div v-if="role == 1" class="teacher-courses">
        <h2>МОИ КУРСЫ</h2>
        <button @click="navigateTo('/createCourse')">Создать курс</button>
        <button @click="openStudentRegistrationModal">Зарегистрировать студента</button>
        <AddStudentModal ref="addStudentModalRef" />
        <!-- Список курсов -->
        <div v-if="courses.length > 0" class="courses-list">
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
        <div v-if="coursesForStudent.length > 0" class="courses-list">
            <div v-for="course in coursesForStudent" class="course-card">
                <img :src="course.picture" alt="Картинка курса" class="course-image"
                    @click="navigateTo(`/courseForStudent/${course.id}`)" />
                <div class="course-info">
                    <h3 style="cursor: pointer;">{{ course.name }}</h3>
                    <p> Прогресс{{ course.progress }} %</p>
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
}

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

<style scoped>
.teacher-courses {
    max-width: 800px;
    margin: 20px auto;
}

.courses-list {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.course-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1px solid #ccc;
    padding: 10px;
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease-in-out;
    width: calc(50% - 10px);
    background-color: #fff;
}

.course-card:hover {
    transform: scale(1.02);
}

.course-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    margin-bottom: 10px;
    cursor: pointer;
}

.course-info {
    text-align: center;
}

.no-courses {
    text-align: center;
    font-size: 18px;
    color: #666;
}
</style>