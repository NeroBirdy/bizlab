<template>
  <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
    <div class="modal">
      <h1>{{ !action ? `Добавление ${!props.role ? 'ученика' : 'учителя'} на курс` : `Удаление ${!props.role ? 'ученика' : 'учителя'} с курса` }}</h1>

      <!-- Поле поиска -->
      <input ref="searchInput" type="text" v-model="searchQuery" placeholder="Искать по ФИО или email" class="input"
        @focus="showDropdown = true" @blur="hideDropdownWithDelay" @keydown.down="onArrowDown" @keydown.up="onArrowUp"
        @keydown.enter="onEnter" />

      <!-- Выпадающий список -->
      <div v-if="showDropdown && filteredUsers.length > 0" class="dropdown">
        <div class="dropdown-list">
          <div v-for="(user, index) in filteredUsers" :key="user.id" class="dropdown-item"
            :class="{ selected: selectedOptionIndex === index }" @click="selectUserFromList(user)"
            @mouseenter="selectedOptionIndex = index">
            {{ user.FIO }} — {{ user.email }}
          </div>
        </div>
      </div>

      <!-- Кнопки управления -->
      <div class="modal-buttons">
        <button @click="closeModal">Закрыть</button>
        <button @click="addSelectedUser" :disabled="!selectedUser">
          {{ !action ? 'Добавить' : 'Удалить'}}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { jwtDecode } from "jwt-decode";
import axios from "axios";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

// === Переменные ===
const showModal = ref(false);
const users = ref<{ id: number; FIO: string; email: string }[]>([]);
const searchQuery = ref("");
const showDropdown = ref(false);
const selectedOptionIndex = ref<number | null>(null);
const selectedUser = ref<{ id: number; FIO: string; email: string } | null>(
  null
);
const userId = ref<number | null>(null);
const selectedCourse = ref();
const userText = ref()

const props = defineProps<{
  role: Number,
  action: Number,
}>();

const fetchUserData = async () => {
  const token = useCookie("auth_token").value;

  if (!token) {
    console.error("Токен отсутствует");
    return;
  }

  try {
    const decodedToken = jwtDecode(token);
    userId.value = decodedToken.user_id || null;

  } catch (error) {
    console.error("Ошибка при декодировании токена:", error);
  }
};

// === Получение пользователей с сервера ===
const getUsers = async (courseId: number) => {
  try {
    let response;
    if (props.role == 0) {
      response = await axios.get(
        `${apiBase}/api/getUsersByCourse`,
        {
          params: {
            courseId: courseId,
            action: props.action
          }
        }
      );
    } else {
      response = await axios.get(
        `${apiBase}/api/getTeachersForCourse`,
        {
          params: {
            courseId: courseId,
            action: props.action,
            userId: userId.value
          }
        }
      );
    }

    users.value = response.data.users || [];
  } catch (error) {
    console.error("Ошибка при загрузке пользователей:", error);
  }
};

// === Фильтр поиска по ФИО и email ===
const filteredUsers = computed(() => {
  if (!searchQuery.value) return [];

  const query = searchQuery.value.toLowerCase();
  return users.value.filter(
    (user) =>
      user.FIO.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query)
  );
});

// === Управление клавиатурой ===
const onArrowDown = () => {
  if (filteredUsers.value.length === 0) return;

  if (
    selectedOptionIndex.value === null ||
    selectedOptionIndex.value >= filteredUsers.value.length - 1
  ) {
    selectedOptionIndex.value = 0;
  } else {
    selectedOptionIndex.value++;
  }

  updateSearchInput();
};

const onArrowUp = () => {
  if (filteredUsers.value.length === 0) return;

  if (selectedOptionIndex.value === null || selectedOptionIndex.value <= 0) {
    selectedOptionIndex.value = filteredUsers.value.length - 1;
  } else {
    selectedOptionIndex.value--;
  }

  updateSearchInput();
};

const onEnter = () => {
  if (
    selectedOptionIndex.value !== null &&
    filteredUsers.value[selectedOptionIndex.value]
  ) {
    selectUserFromList(filteredUsers.value[selectedOptionIndex.value]);
  }
};

const updateSearchInput = () => {
  if (
    selectedOptionIndex.value !== null &&
    filteredUsers.value[selectedOptionIndex.value]
  ) {
    const user = filteredUsers.value[selectedOptionIndex.value as number];
    searchQuery.value = `${user.FIO} — ${user.email}`;
  }
};

// === Выбор пользователя из списка (не добавляем сразу) ===
const selectUserFromList = (user: {
  id: number;
  FIO: string;
  email: string;
}) => {
  selectedUser.value = user;
  searchQuery.value = `${user.FIO} — ${user.email}`;
  showDropdown.value = false;
};

// === Добавление пользователя на курс (по кнопке) ===
const addSelectedUser = async () => {
  if (!selectedUser.value || !selectedCourse.value) {
    alert("Выберите пользователя");
    return;
  }
  if (!props.action) {
    try {

      await axios.post(`${apiBase}/api/inviteUserOnCourse`, {
        courseId: selectedCourse.value,
        userId: selectedUser.value.id,
        role: props.role
      });

      alert(`Пользователь ${selectedUser.value.FIO} успешно добавлен на курс`);
      closeModal();
    } catch (error) {
      console.error("Ошибка при добавлении пользователя:", error);
      alert("Не удалось добавить пользователя");
    }
  } else {
    try {
      if (props.role == 0) {
        await axios.post(`${apiBase}/api/deleteUserFromCourse`, {
          courseId: selectedCourse.value,
          userId: selectedUser.value.id,
        });
      } else {
        await axios.post(`${apiBase}/api/deleteTeacherFromCourse`, {
          courseId: selectedCourse.value,
          userId: selectedUser.value.id,
        });
      }
      alert(`Пользователь ${selectedUser.value.FIO} успешно удален с курса`);
      closeModal();
    } catch (error) {
      console.error("Ошибка при добавлении пользователя:", error);
      alert("Не удалось добавить пользователя");
    }
  }

};

// === Открытие/закрытие модального окна ===
const openModal = (courseId: number) => {
  console.log(courseId);
  selectedCourse.value = courseId;
  showModal.value = true;
  selectedOptionIndex.value = null;
  selectedUser.value = null;
  if (users.value.length === 0) getUsers(courseId);

  // Автофокус
  nextTick(() => {
    searchInput.value?.focus();
  });
};

const closeModal = () => {
  showModal.value = false;
  searchQuery.value = "";
  showDropdown.value = false;
  selectedOptionIndex.value = null;
  selectedUser.value = null;
};

// === Задержка перед скрытием выпадающего списка ===
const hideDropdownWithDelay = () => {
  setTimeout(() => {
    showDropdown.value = false;
  }, 200);
};

// Для фокуса
const searchInput = ref<HTMLInputElement | null>(null);

onMounted(async () => {
  await fetchUserData();
});

defineExpose({ openModal });
</script>

<style scoped>
h1 {
  font-size: 24px;
  font-family: "Uncage";
}

.input {
  border: 2px solid black;
  border-radius: 5px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
  position: relative;
}

.modal input {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  margin-bottom: 10px;
}

/* === Выпадающий список с прокруткой === */
.dropdown {
  position: absolute;
  width: calc(100% - 2px);
  /* совпадает с шириной поля ввода */
  max-height: 120px;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-top: none;
  background-color: white;
  z-index: 1000;
  margin-top: 2px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.dropdown-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown-item {
  padding: 10px;
  cursor: pointer;
}

.dropdown-item.selected {
  background-color: #d7ecff;
}

.dropdown-item:hover {
  background-color: #f0f0f0;
}

/* === Кнопки === */
.modal-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 10px;
}

.modal-buttons button {
  padding: 10px 20px;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.modal-buttons button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}
</style>
