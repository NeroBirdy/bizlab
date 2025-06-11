<template>
    <div class="modal-overlay" v-if="show" @click.self="closeModal">
        <div class="modal">
            <div class="course-buttons flex gap-12 second-half justify-center">
                <p @click="description = true" :class="{ active: description }">
                    Описание
                </p>
                <p v-if="course.compounds.length != 0" @click="description = false" :class="{ active: !description }">
                    Что входит в курс
                </p>
            </div>
            <div class="">
                <div class="">
                    <div class="">
                        <div class="course-text-area">
                            <div v-if="description" class="text-area">
                                {{ course.description }}
                            </div>
                            <div v-else v-for="compound in course.compounds" class="course-compounds">
                                <ul>
                                    <li>{{ compound.name }}</li>
                                </ul>
                            </div>
                        </div>
                        <div class="price-area">
                            <div class="prices">
                                    <p style="
                              text-decoration: line-through;
                            ">
                                        {{ fixprice(course.price) }} ₽
                                    </p>
                                    <p style="
                            ">
                                        {{ fixprice(course.salePrice) }} ₽
                                    </p>
                                    <p class="">в расрочку от
                                        {{ fixprice(course.credit) }} руб/мес</p>
                                          <div class="course-link">
                        <div class=""><a href="#feedback" @click="closeModal">Записаться</a></div>
                    </div>
                            </div>
                        </div>
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
    // padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    width: 95%;
    position: relative;
    height: 70vh;
}

.course-text-area {
    width: 100%;
    height: max-content;
    display: flex;
    flex-direction: column;
    margin-bottom: 5vw;
}

.course-compounds {
    margin: 0 4.7vw;
    display: flex;
    justify-content: end;
    ul {
        width: 90%;
        li {
            list-style-type:circle;
        }
    }
}

.text-area {
    width: 90%;
    height: max-content;
    overflow: scroll;
    margin: 0 auto;
}

.price-area {
    display: flex;
    justify-content: end;
    margin-bottom: 6vw;
}

.prices {
    width: 50%;
    p {
        text-align: end;
        padding: 0 4vw;
        font-size: 4vw;
    }
}

.prices p:nth-child(2) {
    font-size: 5vw;
}

.prices p:nth-child(3) {
    font-size: 2.8vw;
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
    font-size: 3.5vw;
    border-radius: 50px;
    padding: 5px 15px;
    color: white;
    width: 40vw;
    text-align: center;
    justify-content: center;
    // height: 6vw;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: "UnboundedRegular";
    margin: 0 auto;
}

.course-buttons {
    margin: 0;
    font-size: 3vw;
    border-radius: 50px;
    padding: 5px 15px;
    align-items: center;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: "UnboundedRegular";
    cursor: pointer;
    height: 7vh;
    p {
        font-size: 3vw;
    }
}

.active {
    background-color: #328862;
    font-size: 4vw;
    border-radius: 50px;
    padding: 5px 15px;
    color: white;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-family: "UnboundedRegular";
}

@media (max-width: 425px) {
    .course-text-area, .text-area{
        height: 45.7vh;
    }

   

    .price-area{
        justify-content: start;

        *{
            width: 100%;
        }
    }

         .course-link{
        width: 60%;
        margin-top:10px;
    }
}

</style>