<template>
    <h1 class="text-center">ОТЗЫВЫ НАШИХ клиентов</h1>
    <div class="container">
        <swiper-container ref="containerRef">
            <swiper-slide v-for="(course, idx) in courses" :key="idx">
                <div class="course-card">
                    <div class="main-info">
                        <div class="picture-block">
                            <h3>«{{ course.name }}»</h3>
                            <img class ="course-picture" :src="course.picture" alt="Здесь должна быть картинка">
                            <sub>в расрочку от {{ course.credit }} руб/мес</sub>
                        </div>
                        <div class="text-block">
                            <div class="course-buttons flex gap-4">
                                <p @click="description=true " :class="{'active': description}">Описание</p>
                                <p @click="description=false" :class="{'active': !description}">Что входит в курс</p>
                            </div>
                            <div v-if="description" class="course-description">{{ course.description }}</div>
                            <div v-else v-for="compound in course.compounds" class ="course-compounds">
                                <p>{{ compound.name }}</p>
                            </div>
                            <div class="course-places">
                                <p>{{ course.places }} мест </p>
                            </div>
                            <a href="#">Записаться</a>
                            <div class="course-prices">
                                <p style="text-decoration: line-through;">{{ course.price }}</p>
                                <p>{{ course.salePrice }}</p>
                                <p>*{{ course.price }}</p>
                            </div>
                        </div>
                    </div>
                    <div></div>
                </div>
            </swiper-slide>
        </swiper-container>
    </div>

    <button @click="swiper.prev()">
        Prev
    </button>
    <!-- Go forward one slide -->
    <button @click="swiper.next()">
        Next
    </button>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { jwtDecode } from "jwt-decode";

const containerRef = ref(null)
const slides = ref(Array.from({ length: 10 }))

const swiper = useSwiper(containerRef)

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const courses = ref()
const description = ref(true);

const getCourses = async () => {
    const response = await axios.get(`${apiBase}/api/getCourseForMain`, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    console.log(response.data)
    courses.value = response.data;
};


onMounted(() => {
    getCourses();
});

</script>

<style lang="scss" scoped>
.main-info {
    @apply flex;

    .picutre-block{
        width: 40%;
    }

    .text-block{
        margin-left:2%;
        width: 60%;
    }
}

.active{
    color: green;
}

.picture-block{
    h3{
        font-size: 40px;
        color: #3840A9;
    }

    img{
        width: 500px;
        height: 386px;
        top: 239px;
        left: 276px;
        border-radius: 48px;

    }
}

.picture-block{
    .course-description{
        min-height: 80%;
    }
}

</style>