<template>
    <div class="question" v-for="(question, index) in test">
        <h1>Вопрос {{ index }} {{ question.question }}</h1>
        <img v-if="question.image != '-'" class="question-image" :src=question.image alt="">
        <div class="question-answers" v-if="question.type!='open'" v-for="(answer, ans_index) in question.answers">
            <label v-if="question.type != 'open'" :for="`${index}_${ans_index}`">
                <input v-if="question.type == 'single'" type="radio" :id="`${index}_${ans_index}`"
                    :checked="selectedAnswers[index]?.includes(ans_index)" :value=ans_index
                    @click="handleAnswer('single', index, ans_index)">
                <input v-else-if="question.type == 'multiple'" type="checkbox" :id="`${index}_${ans_index}`"
                    :checked="selectedAnswers[index]?.includes(ans_index)" :value=ans_index
                    @click="handleAnswer('multiple', index, ans_index)">
                {{
                    answer.text }}</label>
        </div>
        <input v-else type="text" :id="`${index}_${ans_index}`" @change="handleOpenAnswer(index, $event)">
    </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const route = useRoute()
const materialId = route.params.id;
const test = ref()
const selectedAnswers = ref([])

const handleAnswer = (type, questionIndex, answerIndex) => {
    let currentAnswers = []
    if (type == 'single') {
        currentAnswers.push(answerIndex)
    } else {
            currentAnswers = selectedAnswers.value[questionIndex] || []
        if (currentAnswers.includes(answerIndex)) {
            // Удаляем, если уже выбран
            const i = currentAnswers.indexOf(answerIndex)
            if (i > -1) currentAnswers.splice(i, 1)
        } else {
            // Добавляем, если не выбран
            currentAnswers.push(answerIndex)
        }
    }

    selectedAnswers.value[questionIndex] = currentAnswers
    console.log(selectedAnswers.value)
};

const handleOpenAnswer = (index, input) => {
    selectedAnswers.value[index] = input;
};

const getTest = async (matId) => {
    const response = await axios.post(`${apiBase}/api/parseFile`, { matId })

    test.value = response.data;
    console.log(test.value)
};

onMounted(() => {
    getTest(materialId);
});
</script>

<style lang="scss" scoped></style>