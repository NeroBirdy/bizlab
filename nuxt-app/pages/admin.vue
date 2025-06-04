<template>
    <div>
        <header class="flex w-full h-full justify-between items-center relative">
            <img class="logo" src="/assets/images/bizlap-logo.svg" alt="bizlab" />
            <h1>АДМИНИСТРАТОР</h1>
            <p>выйти из личного кабинета</p>
        </header>
    </div>
    <div>
        <button class="btn btn-primary" @click="openRegisterTeacherModal">добавить преподавателя</button>
        <AddTeacher ref="registerTeacherRef" />
        <button class="btn btn-secondary" @click="openDeleteTeacherModal">удалить преподавателя</button>
        <deleteTeacher ref="deleteTeacherRef" />
    </div>
    <div></div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { jwtDecode } from "jwt-decode";
import deleteTeacher from '../components/deleteTeacher.vue'
import AddTeacher from '../components/AddTeacher.vue'

const deleteTeacherRef = ref()
const registerTeacherRef = ref()

const openDeleteTeacherModal = () => {
    deleteTeacherRef.value?.openModal()
}

const openRegisterTeacherModal = () => {
    registerTeacherRef.value?.openModal()
}


</script>

<style lang="scss"></style>