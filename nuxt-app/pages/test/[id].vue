<template>
    <div class="question" v-for="(question, index) in test">
        <h1>Вопрос {{ index }} {{ question.question }}</h1>
        <img v-if="question.image != '-'" class="question-image" :src=question.image alt="">
        <div class="question-answers" v-if="question.type != 'open'" v-for="(answer, ans_index) in question.answers">
            <label v-if="question.type != 'open'" :for="`${index}_${ans_index}`">
                <input v-if="question.type == 'single'" type="radio" :id="`${index}_${ans_index}`"
                    :checked="selectedAnswers[index]?.includes(answer)" :value=ans_index
                    @click="handleAnswer('single', index, answer)">
                <input v-else-if="question.type == 'multiple'" type="checkbox" :id="`${index}_${ans_index}`"
                    :checked="selectedAnswers[index]?.includes(answer)" :value=ans_index
                    @click="handleAnswer('multiple', index, answer)">
                {{
                    answer.text }}</label>
        </div>

        <input v-else type="text" @change="handleOpenAnswer(index, $event)">
    </div>
    <Button @click="welcomeToTeacher">Отправить</Button>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { jwtDecode } from 'jwt-decode'

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const route = useRoute()
const materialId = route.params.id;
const test = ref()
const selectedAnswers = ref([])
const userId = ref()

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

    } catch (error) {
        console.error('Ошибка при декодировании токена:', error)
    }
}

const handleAnswer = (type, questionIndex, answer) => {
    let currentAnswers = []
    if (type == 'single') {
        currentAnswers.push(answer)
    } else {
        currentAnswers = selectedAnswers.value[questionIndex] || []
        if (currentAnswers.includes(answer)) {
            const i = currentAnswers.indexOf(answer)
            if (i > -1) currentAnswers.splice(i, 1)
        } else {
            currentAnswers.push(answer)
        }
    }

    selectedAnswers.value[questionIndex] = currentAnswers
    console.log(selectedAnswers.value)
};

const handleOpenAnswer = (index, input) => {
    const answers = test.value[index].answers;
    const ans = input.target.value;
    const flag = answers.some((answer) => {
        if (answer.text.toString().toLowerCase() == ans.toString().toLowerCase()) {
            return true;
        }
        return false;
    });
    selectedAnswers.value[index] = { 'text': ans, 'correct': flag };
};

const getTest = async (matId) => {
    const response = await axios.post(`${apiBase}/api/parseFile`, { matId })

    test.value = response.data;
    console.log(test.value)
};

const welcomeToTeacher = async () => {
    let questions = []
    test.value.forEach(question => {
        questions.push(question.question)
    });
    const response = await axios.post(`${apiBase}/api/welcomeToTeacher`, { 'userId': userId.value, 'matId': materialId, 'test': selectedAnswers.value, 'questions': questions });
    navigateTo('/course');
};

onMounted(async () => {
    await fetchUserData();
    await getTest(materialId);
});
</script>

<style lang="scss" scoped></style>