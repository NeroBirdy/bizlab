<template>
    <div class="homeworks-page">

        <!-- Список домашних работ -->
        <div v-if="loading" class="loading">
            Загрузка...
        </div>
        <div v-else-if="homeworks.length === 0" class="no-homeworks">
            Нет домашних работ для проверки
        </div>
        <div v-else class="homework-list">
            <div v-for="homework in homeworks" :key="homework.id" class="homework-item">
                <!-- Аватар студента -->
                <img :src="getAvatar(homework.fio)" alt="Аватар студента" class="student-avatar" />

                <!-- Информация о домашней работе -->
                <div class="homework-info">
                    <p>{{ homework.fio }}</p>
                    <p>Урок: {{ homework.lessonName }}</p>
                    <p>Домашняя работа: {{ homework.materialName }}</p>
                </div>

                <!-- Кнопки -->
                <div class="buttons">
                    <button @click="downloadFile(homework.file)">Скачать</button>
                    <button @click="markAsChecked(homework.id)" :class="{ checked: homework.checked }">
                        {{ homework.checked ? 'Проверено' : 'Проверить' }}
                    </button>
                </div>

                <!-- Иконка состояния -->
                <div class="status-icon">
                    <span v-if="homework.checked" class="checked-icon">✓</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

// === Переменные ===
const loading = ref(true)
const homeworks = ref<{ id: number; fio: string; lessonName: string; materialName: string; file: string; checked: boolean }[]>([])
const courseId = Number(useRoute().params.courseId)
const courseName = ref('')

// === Получение данных курса ===
const getCourseDetails = async () => {
    try {
        // const response = await axios.get(`${apiBase}/api/getCourseDetails/${courseId}`)
        courseName.value = 'Тест'
    } catch (error) {
        console.error('Ошибка при получении данных курса:', error)
    }
}

// === Получение домашних работ ===
const getHomeworks = async () => {
    try {
        console.log(courseId)
        const response = await axios.post(`${apiBase}/api/homework`, { 'courseId': courseId })
        homeworks.value = response.data.homeworks.map(hw => ({
            ...hw,
            checked: false // Добавляем состояние "проверено"
        }))
    } catch (error) {
        console.error('Ошибка при получении домашних работ:', error)
    } finally {
        loading.value = false
    }
}

// === Обработчики событий ===
const downloadFile = async (fileUrl: string) => {
    // const response = await axios.post(`${apiBase}/api/download`, { 'path': fileUrl })

    const response = await fetch(`${apiBase}/api/download`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Authorization: 'Bearer ваш_токен' — если нужна авторизация
      },
      body: JSON.stringify({ path: fileUrl }),
    })

    if (!response.ok) {
      throw new Error('Ошибка при получении файла')
    }

    // Получаем файл как Blob
    const blob = await response.blob()

    let tmp = fileUrl.split('/')

    const fileName = tmp[tmp.length - 1] 

    // Создаём временную ссылку и "клик"
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = fileName
    document.body.appendChild(a)
    a.click()
    a.remove()
    window.URL.revokeObjectURL(url)
}

const markAsChecked = (homeworkId: number) => {
    const homework = homeworks.value.find(hw => hw.id === homeworkId)
    if (homework) {
        homework.checked = !homework.checked
        alert(`Домашняя работа ${homework.fio} помечена как "${homework.checked ? 'проверенная' : 'не проверенная'}"`)
    }
}

// === Генерация аватара по ФИО ===
const getAvatar = (fio: string) => {
    return `/avatars/${fio}.png` // Пример пути к аватару
}

// === Инициализация ===
onMounted(async () => {
    await getCourseDetails()
    await getHomeworks()
})
</script>

<style scoped>
/* === Основные стили === */
.homeworks-page {
    max-width: 800px;
    margin: 20px auto;
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

.homework-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.homework-item {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    position: relative;
}

.student-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 10px;
}

.homework-info {
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

.buttons button.checked {
    background-color: #2ecc71;
}

.status-icon {
    position: absolute;
    top: 10px;
    right: 10px;
}

.checked-icon {
    background-color: #2ecc71;
    color: white;
    border-radius: 50%;
    padding: 5px;
    font-weight: bold;
}
</style>