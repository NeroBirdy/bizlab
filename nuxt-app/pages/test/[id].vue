<template>
  <BizlabLogo />
  <Backimages :variable="3" />
  <div class="text-container">
    <h1 class="text-center text-name">Тест</h1>
    <div class="question" v-for="(question, index) in test">
      <h1 class="quest-id">Вопрос {{ index + 1 }}</h1>
      <h1 class="pl-5 quest-question">{{ question.question }}</h1>
      <div :class="question.image != '-' ? 'image-block' : 'default-block'">
        <Image
          v-if="question.image != '-'"
          class="question-image pl-10 pr-10"
          :src="question.image"
          alt=""
          preview
        />
        <div class="flex flex-col gap-2">
          <div
            class="question-answers pl-10"
            v-if="question.type != 'open'"
            v-for="(answer, ans_index) in question.answers"
          >
            <label
              v-if="question.type != 'open'"
              :for="`${index}_${ans_index}`"
              class="question-label"
            >
              <input
                type="radio"
                v-if="question.type == 'single'"
                :id="`${index}_${ans_index}`"
                :checked="selectedAnswers[index]?.includes(answer)"
                :value="ans_index"
                @click="handleAnswer('single', index, answer)"
              />
              <Checkbox
                v-else-if="question.type == 'multiple'"
                :id="`${index}_${ans_index}`"
                :checked="selectedAnswers[index]?.includes(answer)"
                :value="ans_index"
                @click="handleAnswer('multiple', index, answer)"
                size="large"
              />
              {{ answer.text }}</label
            >
          </div>
          <div v-else class="flex justify-center">
            <input
              type="text"
              @change="handleOpenAnswer(index, $event)"
              class="question-input pl-1 pr-1"
            />
          </div>
        </div>
      </div>
    </div>
    <Button @click="welcomeToTeacher" class="btn">Отправить</Button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const route = useRoute();
const materialId = route.params.id;
const test = ref();
const selectedAnswers = ref([]);
const userId = ref();

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
  } catch (error) {
    console.error("Ошибка при декодировании токена:", error);
  }
};

const handleAnswer = (type, questionIndex, answer) => {
  let currentAnswers = [];
  if (type == "single") {
    currentAnswers.push(answer);
  } else {
    currentAnswers = selectedAnswers.value[questionIndex] || [];
    if (currentAnswers.includes(answer)) {
      const i = currentAnswers.indexOf(answer);
      if (i > -1) currentAnswers.splice(i, 1);
    } else {
      currentAnswers.push(answer);
    }
  }

  selectedAnswers.value[questionIndex] = currentAnswers;
  console.log(selectedAnswers.value);
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
  selectedAnswers.value[index] = { text: ans, correct: flag };
};

const getTest = async (matId) => {
  const response = await axios.post(`${apiBase}/api/parseFile`, { matId });

  test.value = response.data;
  console.log(test.value);
};

const welcomeToTeacher = async () => {
  let questions = [];
  test.value.forEach((question) => {
    questions.push(question.question);
  });
  const response = await axios.post(`${apiBase}/api/welcomeToTeacher`, {
    userId: userId.value,
    matId: materialId,
    test: selectedAnswers.value,
    questions: questions,
  });
  navigateTo("/course");
};

onMounted(async () => {
  await fetchUserData();
  await getTest(materialId);
});
</script>

<style lang="scss" scoped>
.quest-question {
  border-bottom: 1px solid #ccc;
  margin-bottom: 10px;
  border-top: 1px solid #ccc;
}

.quest-id {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px 5%;
  margin-top: 10px;
  border-radius: 5px;
  background-color: #3288624a;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.301);
}

.question-image {
  width: 50%;
}

.btn {
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  font-family: "Uncage";
  font-size: 18px;
  color: white;
  border: none;
  padding: 5px 15px;
  border-radius: 25px;
  height: max-content;
  cursor: pointer;
  background-color: #328862;
  transition: all 0.2s;
  &:hover {
    transform: translateY(-5px) scale(1.05);
    opacity: 70%;
  }
}

.text-name {
  font-size: 24px;
  border-bottom: 2px solid #ccc;
}

.text-container {
  width: 50%;
  margin-left: auto;
  margin-right: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: center;
  background-color: rgba(236, 236, 236, 0.7);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 20px auto;
  font-family: Arial, sans-serif;
}

.question {
  width: 80%;
  background-color: rgb(255, 255, 255);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  font-family: "Inter";

  h1 {
    font-size: 20px;
  }
}

.question-answers {
  font-family: "Inter";
  font-size: 18px;
}

.question-label {
  display: flex;
  align-items: center;
  gap: 5px;
  input[type="radio"] {
    width: 20px !important;
    height: 20px !important;
    min-width: 20px;
    max-width: 20px;
    min-height: 20px;
    max-height: 20px;
    position: relative;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    outline: none;

    &::before {
      content: "";
      position: absolute;
      top: 50%;
      left: 50%;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      transform: translate(-50%, -50%);
      background-color: white;
      border: 2px solid #e5e7eb;
    }

    &:checked::before {
      border: 5px solid #10b981;
    }
  }
}

.question-input {
  width: 90%;
  display: flex;
  justify-content: center;
  border: 2px solid #338862;
  border-radius: 5px;
  font-size: 18px;
  font-family: "Inter";
  height: 50px;
}

.image-block {
  display: flex;
  gap: 4px;
  * {
    padding: 0;
  }

  img {
    width: 40%;
    height: 40%;
    border-radius: 5px;
  }
}
</style>
