<template>
  <div class="relative content">
    <img src="/assets/images/welcomePage/grown.png" class="vector one desktop" />
    <img src="/assets/images/welcomePage/town.png" class="vector two desktop" />

    <div class="container desktop">
      <h1 class="text-center">Курсы</h1>
      <div class="flex justify-between">
        <button @click="swiper.prev()" class="arrow">
          <img src="/assets/images/welcomePage/arrow-prev.svg" style="width: 3vw;"/>
        </button>
        <ClientOnly>
          <swiper-container
            ref="containerRef"
            class="swiper-container"
            pagination="true"
          >
            <swiper-slide
              lazy="true"
              v-for="(course, idx) in courses"
              :key="idx"
              class="slide"
            >
              <p class="course-places">{{ course.places }} мест</p>
              <div class="course-card">
                <div class="main-info">
                  <div class="title flex half-prop">
                    <div class="first-half items-center">
                      <h3 class="text-center">«{{ course.name }}»</h3>
                    </div>
                    <div class="course-buttons flex gap-4 second-half">
                      <p
                        @click="description = true"
                        :class="{ active: description }"
                      >
                        Описание
                      </p>
                      <p
                        v-if="course.compounds.length != 0"
                        @click="description = false"
                        :class="{ active: !description }"
                      >
                        Что входит в курс
                      </p>
                    </div>
                  </div>

                  <div class="info-block half-prop flex">
                    <div class="picture-block first-half">
                      <img
                        loading="lazy"
                        class="course-picture"
                        :src="course.picture"
                        alt="Здесь должна быть картинка"
                      />
                      <sub
                        class="justify-center flex mt-5"
                        style="font-size: 1.4vw"
                        >в расрочку от
                        {{ fixprice(course.credit) }} руб/мес</sub
                      >
                    </div>
                    <div class="text-block hide-scrollbar">
                      <div v-if="description" class="course-description">
                        {{ course.description }}
                      </div>
                      <div
                        v-else
                        v-for="compound in course.compounds"
                        class="course-compounds"
                      >
                        <p>{{ compound.name }}</p>
                      </div>
                    </div>
                  </div>

                  <div class="price-info half-prop flex justify-end mt-5">
                    <div class="second-half">
                      <div class="flex justify-between">
                        <div class="course-link">
                          <a href="#feedback">Записаться</a>
                        </div>
                        <div class="last-price">
                          <p
                            style="
                              text-decoration: line-through;
                              font-size: 1.6vw;
                            "
                          >
                            {{ fixprice(course.price) }} ₽
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="course-prices half-prop flex justify-end">
                    <div class="second-half flex justify-end">
                      <div class="flex-row justify-end price">
                        <p>{{ fixprice(course.salePrice) }} ₽</p>
                        <sup style="font-size: 1vw">*{{ course.sale }}</sup>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </swiper-slide>
          </swiper-container>
        </ClientOnly>
        <button @click="swiper.next()">
          <img src="/assets/images/welcomePage/arrow-next.svg" class="arrow" style="width: 3vw; z-index: 3;"/>
        </button>
      </div>
    </div>
  </div>
  <div class="mobile content-mobile">
    <img src="/assets/images/welcomePage/grown.png" class="vector one" />
    <img src="/assets/images/welcomePage/town.png" class="vector two" />
    <h1 class="text-center">Курсы</h1>
    <ClientOnly>
      <CourseDesc ref="courseDescRef" ></CourseDesc>
        <swiper-container ref="containerRef" class="swiper-container">
          <swiper-slide
            lazy="true"
            v-for="(course, idx) in courses"
            :key="idx"
            class="slide"
          >
            <div class="course-card" @click="openFullCourse(course)">
              <div class="main-info">
                <div class="mini-picture">
                  <div class="">
                    <img
                      loading="lazy"
                      class="course-picture"
                      :src="course.picture"
                      alt="Здесь должна быть картинка"
                    />
                  </div>
                </div>
                <div class="mini-info-container">
                  <p class="mini-places">{{ course.places }} мест</p>
                  <div class="mini-info-container-bottom">
                    <h3 class="text-center">«{{ course.name }}»</h3>
                    <div class="">
                      <div class="">
                        <div class="">
                          <div class="course-link">
                            <a href="#">Подробнее</a>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </swiper-slide>
        </swiper-container>
      </ClientOnly>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";
import CourseDesc from "./CourseDesc.vue";

const containerRef = ref(null);
const slides = ref(Array.from({ length: 10 }));

const swiper = useSwiper(containerRef, {
  effect: "creative",
  loop: true,
  spaceBetween: 100,
});
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const courses = ref();
const description = ref(true);
const courseDescRef = ref();

const getCourses = async () => {
  const response = await axios.get(`${apiBase}/api/getCourseForMain`, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  courses.value = response.data;
};

const openFullCourse = (course) => {
  courseDescRef.value.openModal(course);
};

onMounted(() => {
  getCourses();
});

const fixprice = (price) => {
  let str = price.toString();

  return str.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
};
</script>

<style lang="scss" scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap");

.course-link {
  background-color: #328862;
  font-size: 1.6vw;
  border-radius: 50px;
  padding: 5px 15px;
  color: white;
  width: 21vw;
  text-align: center;
  justify-content: center;
  height: 3.5vw;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: "UnboundedRegular";
}

.half-prop {
  .first-half {
    width: 40%;
  }

  .second-half {
    width: 60%;
    padding-left: 2%;
  }
}

.vector {
  display: block;
  position: absolute;
  width: 18vw;
}

.one {
  left: 0;
  top: 0;
}

.two {
  bottom: 0;
  top: auto;
  right: 0;
}

h3 {
  font-size: 3vw;
  color: #3840a9;
}

.active {
  background-color: #328862;
  font-size: 1.25vw;
  border-radius: 50px;
  padding: 5px 15px;
  color: white;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: "UnboundedRegular";
}

.last-price {
  text-align: end;
  display: flex;
  justify-content: end;
  align-items: end;

  p {
    height: max-content;
    font-family: "Inter", sans-serif;
  }
}

.picture-block {
  max-height: 20vw;
  img {
    width: 35vw;
    height: auto;
    top: 239px;
    left: 276px;
    border-radius: 48px;
  }
}

.text-block {
  margin-left: 20px;
  border-radius: 5px;
  padding-left: 2%;
  width: 36vw;
  max-height: 22vw;
  overflow: scroll;
}

.hide-scrollbar {
  overflow: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

.course-description {
  white-space: pre-wrap;
  font-size: 1vw;
}

.picture-block {
  .course-description {
    min-height: 80%;
  }
}

.arrow {
  transition: all 0.5s;

  &:hover {
    transform: scale(1.1);
  }
}

.swiper-container {
  width: 90%;
}

.slide {
  padding: 10px;
  // background-color: rgb(223, 235, 247);
  border-radius: 15px;
}

.course-places {
  color: white;
  font-family: "UnboundedRegular";
  font-size: 1vw;
  position: absolute;
  top: 0px;
  right: 0px;
  background-image: url("/assets/images/welcomePage/places_bg.png");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  width: 7vw;
  height: 7vw;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.course-buttons {
  margin: 0;
  font-size: 1.25vw;
  border-radius: 50px;
  padding: 5px 15px;
  align-items: center;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-family: "UnboundedRegular";
  cursor: pointer;
}

.price {
  * {
    margin: 0;
    padding: 0;
  }
  p {
    display: flex;
    justify-content: end;
    text-align: end;
    font-size: 2.2vw;
    font-family: "Inter", sans-serif;
  }
}

.mobile {
  display: none;
  position: relative;
}

@media (max-width: 767px) {
  .desktop, .content {
    display: none;   
  }
  .mobile {
    display: block;
  }
  .main-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .course-picture {
    width: 100%;
    border-radius: 15px;
  }
  .slide {
    justify-items: center;
  }
  .mini-picture {
    max-width: 65%;
  }

  .main-info-container {
    width: 100%;
    display: flex;
  }

  .mini-info-container {
    height: 31vw;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
  }

  .mini-places {
    width: 20vw;
    text-align: center;
    background-color:rgb(226, 93, 53);
    border-radius: 14px;
    font-family: "UnboundedRegular";
    color: white;
    font-size: 2.5vw;
  }

  .mini-info-container-bottom {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 50%;
    justify-content: space-between;
  }
  .swiper-container {
    width: 90%;
  }
}

@media (max-width: 1025px) {
  .picture-block {
    img {
      height: 22vw;
    }
  }
  .text-block {
    height: 27vw;
  }
  .course-description {
    font-size: 1.5vw;
  }
}
</style>
