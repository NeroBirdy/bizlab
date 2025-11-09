<template>
    <BizlabLogo />
    <p class="logout" @click="logout">ВЫЙТИ ИЗ ЛИЧНОГО КАБИНЕТА</p>
    <div class="window-card">
        <div class="admin-card">
            <nav class="nav-buttons">
                <button @click="chooseLogs = false" :class="{ active: !chooseLogs }">
                    Логирование
                </button>
                <button @click="chooseLogs = true" :class="{ active: chooseLogs }">
                    Аналитика
                </button>
            </nav>

            <div v-if="!chooseLogs">
                <h1 class="header">Список авторизаций</h1>
                <div class="table">
                    <div class="inside-table">
                        <div class="row" v-for="log in logs">
                            <div class="column id">
                                <p>{{ log.id }}</p>
                            </div>
                            <div class="column id">
                                <p>{{ log.role == 2 ? "Учитель" : log.role == 1 ? "Ученик" : "Админ" }}</p>
                            </div>
                            <div class="column text">
                                <p>{{ log.name }}</p>
                            </div>
                            <div class="column timestamp">
                                <p>{{ log.created.slice(0, 10).replaceAll('-', '.') + ' ' + log.created.slice(11, 19) }}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="navigator-buttons">
                    <button class="button" :disabled="page == 1" @click="page--; getSearch();">
                        < </button>
                            <button class="button" @click="page++; getSearch();">></button>
                </div>
            </div>
            <div class="anal" v-else>
                <div>
                    <div class="table">
                        <h1>Загруженные файлы</h1>
                        <h1>{{ second.length }}</h1>
                        <div class="inside-table">
                            <div class="row2" v-for="log in second">
                                <div class="column id">
                                    <p>{{ log.id }}</p>
                                </div>
                                <div class="column text">
                                    <p>{{ log.name }}</p>
                                </div>
                                <div class="column timestamp">
                                    <p>{{ log.created.slice(0, 10).replaceAll('-', '.') + ' ' + log.created.slice(11,
                                        19) }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div>
                    <div class="table">
                        <h1>Зарегистрированные пользователи</h1>
                        <h1>{{ third.length }}</h1>
                        <div class="inside-table">
                            <div class="row2" v-for="log in third">
                                <div class="column id">
                                    <p>{{ log.id }}</p>
                                </div>
                                <div class="column text">
                                    <p>{{ log.name }}</p>
                                </div>
                                <div class="column timestamp">
                                    <p>{{ log.created.slice(0, 10).replaceAll('-', '.') + ' ' + log.created.slice(11,
                                        19) }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="table">
                        <h1>Выполненных заданий</h1>
                        <h1>{{ forth.length }}</h1>
                        <div class="inside-table">
                            <div class="row2" v-for="log in forth">
                                <div class="column id">
                                    <p>{{ log.id }}</p>
                                </div>
                                <div class="column text">
                                    <p>{{ log.name }}</p>
                                </div>
                                <div class="column timestamp">
                                    <p>{{ log.created.slice(0, 10).replaceAll('-', '.') + ' ' + log.created.slice(11,
                                        19) }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="table">
                        <h1>Проверенных заданий</h1>
                        <h1>{{ fifth.length }}</h1>
                        <div class="inside-table">
                            <div class="row2" v-for="log in fifth">
                                <div class="column id">
                                    <p>{{ log.id }}</p>
                                </div>
                                <div class="column text">
                                    <p>{{ log.name }}</p>
                                </div>
                                <div class="column timestamp">
                                    <p>{{ log.created.slice(0, 10).replaceAll('-', '.') + ' ' + log.created.slice(11,
                                        19) }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import deleteTeacher from "../components/deleteTeacher.vue";
import AddTeacher from "../components/AddTeacher.vue";

const deleteTeacherRef = ref();
const registerTeacherRef = ref();
const sender = ref();
const text = ref();
const userStore = useAuthStore();
const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;
const chooseLogs = ref(false);
const logs = ref([]);
const page = ref(1);

const second = ref([]);
const third = ref([]);
const forth = ref([]);
const fifth = ref([]);

const fetchUserData = async () => {
    try {
        const formData = new FormData();
        formData.append("page", page.value);
        formData.append("type", "1");
        const response = await axios.post(`${apiBase}/api/getLogs`, formData);
        logs.value = response.data;
        const response2 = await axios.post(`${apiBase}/api/getLogs`, { "page": 1, "type": 2 });
        second.value = response2.data;
        const response3 = await axios.post(`${apiBase}/api/getLogs`, { "page": 1, "type": 3 });
        third.value = response3.data;
        const response4 = await axios.post(`${apiBase}/api/getLogs`, { "page": 1, "type": 4 });
        forth.value = response4.data;
        const response5 = await axios.post(`${apiBase}/api/getLogs`, { "page": 1, "type": 5 });
        fifth.value = response5.data;
    } catch (error) {
        console.error("Ошибка при получении данных:", error);
    }
};

const getSearch = async () => {
    try {
        const formData = new FormData();
        formData.append("page", page.value);
        formData.append("type", "1");
        const response = await axios.post(`${apiBase}/api/getLogs`, formData);
        logs.value = response.data;
    } catch (error) {
        console.error("Ошибка:", error);
    }
};

onMounted(() => {
    fetchUserData();
});

const logout = async () => {
    //   const response = await axios.post(`${apiBase}/api/auth/logout`);
    userStore.logoutUser();
    navigateTo("/");
};

</script>

<style lang="scss" scoped>
.anal {
    margin-top: 20px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr);
    grid-column-gap: 0px;
    grid-row-gap: 20px;
}

.nav-buttons {
    width: 100%;
    display: flex;
    justify-content: space-between;

    button {
        font-family: "Uncage";
        font-size: 24px;
        color: #ff7f50;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;

        &:hover {
            text-decoration: underline;
        }
    }

    .active {
        background-color: #e25d35;
        border-radius: 20px;
        color: white;

        &:hover {
            text-decoration: none;
        }
    }
}

input,
textarea {
    @apply shadow-md;
    height: 30px;
    padding: 5px;
    font-size: 1vw;
    border: 2px solid green;
    border-radius: 5px;
    margin-top: 5px;
    background-color: white;

    &::placeholder {
        color: green;
    }
}

textarea {
    min-height: 30px;
    height: 200px;
}

.buttons-div {
    display: flex;
    // flex-wrap: wrap;
    justify-content: space-evenly;
    padding-bottom: 10px;
    border-bottom: 1px solid #ccc;
    margin-bottom: 10px;
}

.logout {
    cursor: pointer;
    position: absolute;
    top: 2%;
    right: 2%;
    display: flex;
    width: 100px;
    font-family: "Uncage";
    color: #e15d34;
    transition: all 0.5s;

    &:hover {
        transform: translateX(-10px);
    }
}

.header {
    margin-top: 5px;
    margin-bottom: 10px;
}

.button {
    padding: 10px 20px;
    background-color: #39ac78c2;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 16px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.3s ease;

    &:hover {
        background-color: #419e745b;
    }

    .icon {
        margin-left: 10px;
        font-size: 12px;
    }
}

.navigator-buttons {
    margin-top: 10px;
    display: flex;
    justify-content: center;
    gap: 7px;
}

.window-card {
    width: 1000px;
    margin: 20px auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.admin-card {
    // background-color: #3288624A;
    width: 100% !important;
    padding: 15px 30px;
    border-radius: 5px;
    transition: transform 0.2s ease-in-out;
    width: calc(50% - 10px);
}

.header {
    height: max-content;
    display: flex;
    margin: 0;
    align-items: center;
    justify-content: space-between;
    padding: 10px 0;
    width: 100%;
    margin-bottom: 10px;
    margin-left: 100px;

    h1 {
        font-family: "Uncage";
        font-size: 24px;
    }
}

h1 {
    font-family: "Uncage";
    font-size: 16px;
    text-align: center;
}

.btn {
    font-family: "Uncage";
    font-size: 18px;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 25px;
    cursor: pointer;


    transition: all 0.2s;

    &:hover {
        transform: translateY(-5px) scale(1.05);
        opacity: 70%;
    }
}

h2 {
    font-family: "Uncage";
    font-size: 24px;
}

.form-title {
    font-family: "Itern";
    font-size: 20px;
}

@media (max-width: 1025px) {
    .window-card {
        width: 95%;
    }

    .btn-add,
    .btn-delete {
        @apply w-60;
    }
}

@media (max-width: 650px) {
    .buttons-div {
        @apply gap-4;
        align-items: center;
        flex-direction: column;
    }

    .btn-add,
    .btn-delete {
        @apply w-80;
    }

    .btn-div {
        @apply justify-center;
    }
}

@media (max-width: 375px) {
    #sender {
        height: 40px
    }

    .btn-add,
    .btn-delete {
        @apply w-60;
        font-size: 15px;
    }

    h1,
    h2 {
        font-size: 22px !important;
    }
}

.table {
    display: grid;
    // background-color: rgba(201, 201, 201, 0.534);
    background-color: #3288624A;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
    border-radius: 15px;
    // border: 2px solid rgba(141, 141, 141, 0.658);
    // grid-template-rows: 1fr;
    grid-column: 1;
}

.inside-table {
    padding-top: 10px;
    padding: 5px;
}

.row {
    display: grid;
    margin-top: 5px;
    grid-template-columns: 1fr 2fr 3fr 7fr;
}

.row2 {
    display: grid;
    margin-top: 5px;
    grid-template-columns: 1fr 2fr 3fr;
}

.id {
    margin-left: 30%;
    // margin-right: 8%;
}

.idH {
    margin-left: 17%;
    font-weight: bold;
}

.textH {
    width: 80%;
    text-align: center;
    font-weight: bold;
}

.timeH {
    margin-left: 8%;
    font-weight: bold;
}

.text {
    margin-right: 5%;
    text-align: left;
}

.timestamp {
    margin-right: 5%;
    text-align: right;
}
</style>
