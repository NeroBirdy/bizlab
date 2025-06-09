<template>
  <Backimages :variable="2" />
  <BizlabLogo />
  <div class="create-course">
    <h1>Создать курс</h1>

    <form @submit.prevent="handleSubmit">
      <div class="form-image">
        <div class="image-name">
          <div class="image-alt" @click="triggerFileInput">
            <img
              v-if="picturePreview"
              :src="picturePreview"
              alt="Превью товара"
            />
            <span v-else>Загрузите <br />фото <br />курса</span>
          </div>
          <input
            type="file"
            id="product-photo"
            style="display: none"
            ref="fileInput"
            @change="onFileChange"
          />
        </div>
        <div class="description">
          <div class="form-group">
            <label for="name">Название:</label>
            <input type="text" id="name" v-model="name" required />
          </div>

          <div class="form-group">
            <label for="description">Описание:</label>
            <textarea
              id="description"
              v-model="description"
              required
            ></textarea>
          </div>
        </div>
      </div>
      <div class="option-buttons">
        <button
          class="btn"
          type="button"
          @click="commonInfo = true"
          :class="commonInfo ? 'active' : ''"
        >
          Общая информация
        </button>
        <button
          class="btn"
          type="button"
          @click="commonInfo = false"
          :class="commonInfo ? '' : 'active'"
        >
          О чём курс
        </button>
      </div>
      <div class="field-option" v-if="commonInfo">
        <div class="form-group">
          <label for="places">Количество мест:</label>
          <input type="number" id="places" v-model.number="places" required />
        </div>

        <div class="form-group">
          <label for="price">Цена:</label>
          <input
            type="number"
            id="price"
            step="0.01"
            v-model.number="price"
            required
          />
        </div>

        <div class="form-group">
          <label for="salePrice">Цена со скидкой:</label>
          <input
            type="number"
            id="salePrice"
            step="0.01"
            v-model.number="salePrice"
          />
        </div>

        <div class="form-group">
          <label for="sale">Причина акции:</label>
          <input type="text" id="sale" v-model="sale" />
        </div>

        <div class="form-group">
          <label for="credit">Стоймость в рассрочку:</label>
          <input type="number" id="credit" v-model.number="credit" />
        </div>
      </div>
      <!-- Составляющие курса -->
      <div class="form-group" v-else>
        <div
          v-for="(compound, index) in compounds"
          :key="index"
          class="compound-item"
        >
          <input
            type="text"
            v-model="compounds[index]"
            placeholder="Введите составляющую"
            required
          />
          <button
            @click="removeCompound(index)"
            type="button"
            class="remove-button"
          >
            Удалить
          </button>
        </div>
        <button @click="addCompound" type="button" class="add-button">
          Добавить составляющую
        </button>
      </div>

      <!-- Кнопка отправки -->
      <div class="flex justify-end">
        <button type="submit" class="submit-button" v-if="allFieldsFilled">
          Создать курс
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

// === Реактивные поля формы ===
const userId = ref("");
const name = ref("");
const description = ref("");
const places = ref<number | null>(null);
const price = ref<number | null>(null);
const salePrice = ref<number | null>(null);
const sale = ref("");
const credit = ref<number | null>(null);
const picture = ref<File | null>(null);
const compounds = ref<string[]>([""]);
const picturePreview = ref<string | null>(null);
const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;
const commonInfo = ref(true);

const allFieldsFilled = computed(() => {
  return (
    !!name.value.trim() &&
    !!description.value.trim() &&
    places.value !== null &&
    price.value !== null &&
    salePrice.value !== null &&
    !!sale.value.trim() &&
    credit.value !== null &&
    picture.value !== null
  );
});

// Предварительный просмотр изображения
const previewImage = ref<string | null>(null);

// === Обработчики ===
const fileInput = ref(null);
const triggerFileInput = () => {
  fileInput.value.click();
};

// Добавление новой составляющей
const addCompound = () => {
  compounds.value.push("");
};

// Удаление составляющей
const removeCompound = (index: number) => {
  compounds.value.splice(index, 1);
};

// Отправка формы
const handleSubmit = async () => {
  try {
    const form = new FormData();

    form.append("userId", userId.value);
    form.append("name", name.value);
    form.append("description", description.value);
    form.append("places", String(places.value));
    form.append("price", String(price.value));
    form.append("salePrice", String(salePrice.value));
    form.append("sale", sale.value);
    form.append("credit", String(credit.value));

    if (picture.value) {
      form.append("picture", picture.value);
    }

    form.append("compounds", JSON.stringify(compounds.value));

    const response = await axios.post(`${apiBase}/api/createCourse`, form, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    console.log("Курс успешно создан:", response.data);
    alert("Курс успешно создан!");
  } catch (error) {
    if (error.response.data.error == "Курс с таким названием уже существует") {
      alert("Курс с таким названием уже существует");
    } else {
      alert("Ошибка при создании курса. Пожалуйста, попробуйте снова.");
    }
  }
};

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    const file = target.files[0];

    picturePreview.value = URL.createObjectURL(file);
    picture.value = file;
  }
};

const fetchUserData = async () => {
  const token = useCookie<string | null>("auth_token").value;
  try {
    const token = useCookie<string | null>("auth_token").value;
    const decodedToken: any = jwtDecode(token!);

    userId.value = decodedToken.user_id || null;
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
  }
};

onMounted(() => {
  fetchUserData();
});
</script>

<style scoped lang="scss">
.create-course {
  background-color: rgb(236, 236, 236);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 20px auto;
  font-family: "Inter";

  h1 {
    font-family: "Uncage";
    font-size: 24px;
    border-bottom: 1px solid #ccc;
    margin-bottom: 10px;
  }
}

.btn {
  height: 80%;
  border-radius: 5px 5px 0px 0px;
  margin-left: 10px;
  margin-top: 1px;
  padding: 5px 10px;
  font-family: "Uncage";
  font-size: 16px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.option-buttons {
  background-color: #3288624a;
  border-radius: 5px;
  height: 40px;
  display: flex;
  align-items: end;
  margin-bottom: 10px;
  .active {
    background-color: rgba(255, 255, 255, 0.712);
    box-shadow: 0px -2px 8px 0px rgba(34, 60, 80, 0.2);
  }
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.preview-image {
  max-width: 150px;
  margin-top: 10px;
}

.compound-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.compound-item input {
  flex: 1;
  margin-right: 10px;
}

.add-button,
.remove-button {
  padding: 5px 10px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.remove-button {
  background-color: rgb(134, 0, 0);
}

.submit-button {
  padding: 10px 20px;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

#description {
  white-space: pre-wrap;
}

form-image,
.form-info {
  height: 100%;

  @media (max-width: 768px) {
    width: 100% !important;
    height: auto;
  }
}

.form-info {
  width: 80%;

  @media (max-width: 768px) {
    width: 100%;
  }
}

.image-alt {
  cursor: pointer;
  text-transform: uppercase;
  font-size: 24px;
  font-weight: bold;
  color: black;
  border: 2px solid #328862;
  border-radius: 15px;
  height: 260px;
  width: 280px;
  background-color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;

  @media (max-width: 768px) {
    width: 35vw;
    height: 35vw;
    margin: 0 auto;
    font-size: 18px;
  }

  img {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
    border-radius: 10px;
    object-fit: contain;
  }
}

.form-image {
  display: flex;
  .description {
    width: 60%;

    #description {
      min-height: 150px;
      max-height: 600px;
    }
  }
  .image-name {
    width: 40%;
  }
}

@media (max-width: 850px) {
  .create-course {
    margin: 20px;
  }

  .image-name {
    margin-right: 10px;
  }
}

@media (max-width: 560px) {
  .form-image {
    flex-direction: column;

    .image-name {
      width: 100%;

      .image-alt {
        width: 60vw;
        height: 40vw;
        margin-right: auto;
        margin-left: auto;
      }
    }
    .description {
      width: 100% !important;
    }
  }
}

@media (max-width: 450px) {
  .option-buttons {
    height: 40px;

    .btn {
      font-size: 14px;
    }
  }
}

@media (max-width: 375px) {
  .option-buttons {
    height: max-content;
    padding: 0 10px;

    .btn {
      margin: 0;
    }
  }

  .compound-item {
    flex-direction: column;
    gap: 5px;
    justify-content: center;
    input {
      width: 100%;
      margin: 0;
    }
  }

  .add-button {
    width: 100%;
  }
  .form-image {
    .image-name {
      margin-bottom: 10px;
      width: 100%;
      .image-alt {
        width: 100%;
        height: 200px;
        margin: 0;
        padding: 0;
      }
    }
  }
}
</style>
