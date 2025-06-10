<template>
    <div class="modal-overlay" v-if="show">
        <div class="modal">
            <div class="course-buttons flex gap-12 second-half justify-center">
                <p @click="description = true" :class="{ active: description }">
                    Описание
                </p>
                <p v-if="course.compounds.length != 0" @click="description = false" :class="{ active: !description }">
                    Что входит в курс
                </p>
            </div>
            <div class="price-info half-prop flex justify-center mt-5">
                <div class="second-half">
                    <div class="flex justify-between flex-col">
                        <div class="text-block">
                            <div v-if="description" class="course-description">
                                {{ course.description }}
                            </div>
                            <div v-else v-for="compound in course.compounds" class="course-compounds">
                                <p>{{ compound.name }}</p>
                            </div>
                        </div>
                        <div class="bottom">
                            <div class="prices right ">
                                <div class="last-price flex flex-row justify-between">
                                    <p style="
                              font-size: 1.6vw;
                            ">
                                        {{ fixprice(course.salePrice) }} ₽
                                    </p>
                                    <sub class="mt-1" style="font-size: 1.6vw">в расрочку от
                                        {{ fixprice(course.credit) }} руб/мес</sub>
                                </div>
                                <div class="last-price left">
                                    <p style="
                              text-decoration: line-through;
                              font-size: 1.6vw;
                            ">
                                        {{ fixprice(course.price) }} ₽
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="link flex justify-end">
                        <div class="course-link flex justify-end"><a href="#feedback">Записаться</a></div>
                    </div>

                </div>
            </div>
        </div>
    </div>


</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmits, defineExpose, nextTick } from "vue";

const show = ref(false);

const course = ref();
const description = ref(true);

const openModal = (courseCopy: object) => {
    course.value = courseCopy;
    show.value = true;
}

function closeModal() {
    show.value = false;
}

const fixprice = (price) => {
    let str = price.toString();

    return str.replace(/\B(?=(\d{3})+(?!\d))/g, " ");
};

defineExpose({ openModal });
</script>

<style lang="scss" scoped>
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

.link {
    width: 100%;
}

.text-block {
    overflow: scroll;
    max-height: 30%;
}

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

@media (max-width: 425px) {
    .modal {
        width: 95%;
    }
}
</style>