<template>
    <div class="student-course-page">
        <!-- Шапка -->
        <header class="header">
            <img alt="Логотип" class="logo" />
            <h1>{{ courseName }}</h1>
        </header>

        <!-- Основной контент -->
        <div v-if="loading" class="loading">
            Загрузка...
        </div>
        <div v-else>
            <!-- Список уроков -->
            <div v-for="(materials, lessonName) in course" :key="lessonName" class="lesson-card">
                <h2>{{ lessonName }}</h2>

                <!-- Материалы -->
                <ul class="material-list">
                    <li v-for="material in materials" :key="material.id" class="material-item">
                        <span>{{ material.name }}</span>

                        <div v-if="['1', '2'].includes(material.type)">
                            <button @click="downloadFile(material.file)" class="download-button">
                                Скачать
                            </button>
                            <input type="file" :id="'fileInput-' + material.id"
                                @change="handleFileUpload($event, material)" style="display: none" />
                            <label :for="'fileInput-' + material.id" class="attach-button">
                                {{ uploadedFiles[material.id] ? uploadedFiles[material.id] : 'Прикрепить' }}
                            </label>
                        </div>

                        <a v-else-if="material.type == 4" :href="material.link" target="_blank"
                            rel="noopener noreferrer" class="external-link">Перейти по ссылке</a>
                        <a v-else-if="material.type == 3" :href="material.link" target="_blank" class="test-link">
                            Перейти к тесту
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { jwtDecode } from 'jwt-decode'

const config = useRuntimeConfig()
const apiBase = config.public.apiBase as string

// === Переменные ===

const loading = ref(true)
const userId = ref<number | null>(null)
const courseName = ref('')
const course = ref<{
    [lessonName: string]: Array<{
        id: number
        name: string
        type: number
        file?: string
        link?: string
    }>
}>()

const uploadedFiles = ref<{ [materialId: number]: string }>({})

const handleFileUpload = async (event: Event, material: any) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  try {
    const formData = new FormData()
    formData.append('userId', userId.value!.toString())
    formData.append('materialId', material.id.toString())
    formData.append('file', file)

    // Отправка на сервер
    const response = await axios.post(`${apiBase}/api/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    alert('Файл успешно загружен!')

    // Сохраняем имя загруженного файла
    uploadedFiles.value[material.id] = file.name
  } catch (error) {
    console.error('Ошибка при загрузке домашней работы:', error)
    alert('Не удалось загрузить файл')
  }

  // Очистка поля ввода, чтобы можно было повторно загрузить тот же файл
  target.value = ''
}


// === Получение данных курса для студента ===
const getCourseDetails = async () => {
    const token = useCookie('auth_token').value

    if (!token) {
        console.error('Токен отсутствует')
        loading.value = false
        return
    }

    try {
        const decodedToken = jwtDecode(token)
        userId.value = decodedToken.user_id || null // Предполагается, что ID студента хранится в cookie
        const courseId = Number(useRoute().params.courseId)

        const response = await axios.get(`${apiBase}/api/getCourseForUser`, {
            params: {
                'userId': userId.value,
                'courseId': courseId,
            },
        })

        courseName.value = response.data.courseName
        course.value = response.data.course
    } catch (error) {
        console.error('Ошибка при получении данных курса:', error)
    } finally {
        loading.value = false
    }
}

// === Скачивание файла ===
const downloadFile = async (fileUrl: string) => {
    try {
        const response = await axios.post(`${apiBase}/api/download`, {
            path: fileUrl,
        }, {
            responseType: 'blob',
        })

        const blob = new Blob([response.data], { type: response.headers['content-type'] })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = fileUrl.split('/').pop() || 'file'
        document.body.appendChild(a)
        a.click()
        a.remove()
        window.URL.revokeObjectURL(url)
    } catch (error) {
        console.error('Ошибка при скачивании файла:', error)
        alert('Не удалось скачать файл')
    }
}

// === Инициализация ===
onMounted(async () => {
    await getCourseDetails()
})
</script>

<style scoped>
.student-course-page {
    max-width: 800px;
    margin: 20px auto;
    font-family: Arial, sans-serif;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #ccc;
}

.attach-button {
  padding: 6px 12px;
  background-color: #3498db;
  color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
}

.attach-button:hover {
  background-color: #2980b9;
}

.header img {
    width: 150px;
}

.external-link {
    padding: 5px 10px;
    background-color: #2ecc71;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-size: 14px;
}

.external-link:hover {
    background-color: #27ae60;
}

.header h1 {
    font-size: 24px;
    margin: 0;
}

.lesson-card {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
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