<template>
  <div class="relative">
    <img src="/assets/images/welcomePage/grown.png" class="vector one" />
    <img src="/assets/images/welcomePage/town.png" class="vector two" />

    <div class="container">
      <h1 class="text-center">Курсы</h1>
      <div class="flex justify-between">
        <button @click="swiper.prev()" class="arrow">
          <img src="/assets/images/welcomePage/arrow-prev.svg" />
        </button>
        <ClientOnly>
          <swiper-container ref="containerRef" class="swiper-container">
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
                        style="font-size: 20px"
                        >в расрочку от
                        {{ fixprice(course.credit) }} руб/мес</sub
                      >
                    </div>
                    <div class="text-block second-half">
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
                          <a href="#">Записаться</a>
                        </div>
                        <div class="last-price">
                          <p
                            style="
                              text-decoration: line-through;
                              font-size: 24px;
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
                        <sup style="font-size: 14px">*{{ course.sale }}</sup>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </swiper-slide>
          </swiper-container>
        </ClientOnly>
        <button @click="swiper.next()">
          <img src="/assets/images/welcomePage/arrow-next.svg" class="arrow" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

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

const getCourses = async () => {
  const response = await axios.get(`${apiBase}/api/getCourseForMain`, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  courses.value = response.data;
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
  font-size: 24px;
  border-radius: 50px;
  padding: 5px 15px;
  color: white;
  width: 300px;
  text-align: center;
  justify-content: center;
  height: 50px;
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
  font-size: 40px;
  color: #3840a9;
}

.active {
  background-color: #328862;
  font-size: 18px;
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
  img {
    width: 500px;
    height: 386px;
    top: 239px;
    left: 276px;
    border-radius: 48px;
  }
}

.text-block {
  margin-left: 20px;
  border-radius: 5px;
}

.course-description {
  width: 80%;
  white-space: pre-wrap;
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
  background-color: rgb(223, 235, 247);
  border-radius: 15px;
}

.course-places {
  color: white;
  font-family: "UnboundedRegular";
  position: absolute;
  top: 0px;
  right: 0px;
  background-image: url("/assets/images/welcomePage/places_bg.png");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.course-buttons {
  margin: 0;
  font-size: 18px;
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
    font-size: 32px;
    font-family: "Inter", sans-serif;
  }
}
</style>
