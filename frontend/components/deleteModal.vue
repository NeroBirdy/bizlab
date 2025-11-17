<template>
  <div v-if="showModal" class="modal-overlay">
    <div class="modal">
      <h1>Вы действительно хотите удалить данный {{ props.toDelete }}?</h1>
      <div class="modal-buttons">
        <button @click="closeModal">Нет</button>
        <button @click="confirmAction">Да</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineExpose } from "vue";
import axios from "axios";

const config = useRuntimeConfig();
const apiBase = config.public.apiBase as string;

const showModal = ref(false);

const props = defineProps<{
  course: {
    [lessonId: number]: {
      id: number;
      name: string;
      materials: {
        id: number;
        name: string;
        type: string;
      }[];
    };
  };
  elementId: any;
  type: Number;
  toDelete: string;
}>();

const objectName = ref();

const openModal = () => {
  console.log(props.elementId);
  showModal.value = true;
};

function closeModal() {
  showModal.value = false;
}

const confirmAction = async () => {
  if (props.type == 0) {
    deleteMaterial(props.elementId.materialId);
  } else if (props.type == 1) {
    deleteCourse(props.elementId);
  } else {
    removeLesson(props.elementId.lessonId);
  }
};

const deleteMaterial = async (materialId: number) => {
  try {
    await axios.post(`${apiBase}/api/deleteMaterial`, { matId: materialId });

    for (let lesson in props.course) {
      props.course[lesson].materials = props.course[lesson].materials.filter(
        (m: any) => m.id !== materialId
      );
    }
    closeModal();
  } catch (error) {
    console.error("Ошибка при удалении материала:", error);
  }
};

async function deleteCourse(id: number) {
  try {
    const response = await axios.post(
      `
    ${apiBase}/api/deleteCourse`,
      { courseId: id }
    );
    console.log(response);
    closeModal();
    navigateTo("/course");
  } catch (error) {
    console.log(error);
  }
}

const removeLesson = async (lessonId: number) => {
  await axios.post(`${apiBase}/api/deleteLesson`, {
    courseId: props.elementId.courseId,
    lesId: lessonId,
  });
  delete props.course[lessonId];
  closeModal();
};

defineExpose({ openModal });
</script>

<style lang="scss" scoped>
h1 {
  text-align: center;
  font-size: 18px;
  font-family: "Uncage";
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
