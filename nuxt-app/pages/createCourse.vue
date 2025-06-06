<template>
  <div class="create-course">
    <h2>Создать курс</h2>

    <!-- Форма для ввода данных -->
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name">Название:</label>
        <input type="text" id="name" v-model="name" required />
      </div>

      <div class="form-group">
        <label for="description">Описание:</label>
        <textarea id="description" v-model="description" required></textarea>
      </div>

      <div class="form-group">
        <label for="places">Места:</label>
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
        <label for="sale">Акция:</label>
        <input type="text" id="sale" v-model="sale" />
      </div>

      <div class="form-group">
        <label for="credit">Кредиты:</label>
        <input type="number" id="credit" v-model.number="credit" />
      </div>

      <!-- Загрузка изображения -->
      <div class="form-group">
        <label for="picture">Изображение:</label>
        <input
          type="file"
          id="picture"
          @change="handleFileUpload"
          accept="image/*"
          required
        />
        <img
          v-if="previewImage"
          :src="previewImage"
          alt="Предпросмотр изображения"
          class="preview-image"
        />
      </div>

      <!-- Составляющие курса -->
      <div class="form-group">
        <label>Составляющие:</label>
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
          <button @click="removeCompound(index)" class="remove-button">
            Удалить
          </button>
        </div>
        <button @click="addCompound" class="add-button">
          Добавить составляющую
        </button>
      </div>

      <!-- Кнопка отправки -->
      <button type="submit" class="submit-button">Создать курс</button>
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
const compounds = ref<string[]>([]);

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

// Предварительный просмотр изображения
const previewImage = ref<string | null>(null);

// === Обработчики ===

// Добавление новой составляющей
const addCompound = () => {
  compounds.value.push("");
};

// Удаление составляющей
const removeCompound = (index: number) => {
  compounds.value.splice(index, 1);
};

// Обработчик загрузки файла
const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0] || null;

  if (file) {
    picture.value = file;

    // Предварительный просмотр изображения
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImage.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
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
    console.error("Ошибка при создании курса:", error);
    alert("Ошибка при создании курса. Пожалуйста, попробуйте снова.");
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

<style scoped>
.create-course {
  max-width: 600px;
  margin: 20px auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
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
</style>
