<template>
  <div class="background-vectors">
    <img
      v-for="(vec, index) in positions"
      :key="index"
      :src="vec.src"
      :width="vec.width"
      :style="{ position: 'absolute', left: vec.x + 'px', top: vec.y + 'px' }"
      alt="Vector"
    />
  </div>
</template>

<style lang="scss" scoped>
.background-vectors {
  z-index: -1;
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>

<script setup>
import { initPositions } from "~/utils/shuffleback";

const props = defineProps(["variable"]);

const positions = ref([]);
var images;

if (props.variable == 1) {
  images = [
    { src: "/images/vectors/zigzak.png", width: 150 },
    { src: "/images/vectors/town.png", width: 200 },
    { src: "/images/vectors/vector.svg", width: 200 },
    { src: "/images/vectors/grown.png", width: 200 },
    { src: "/images/vectors/zigzak.png", width: 150 },
    { src: "/images/vectors/town.png", width: 200 },
    { src: "/images/vectors/grown.png", width: 200 },
    { src: "/images/vectors/zigzak.png", width: 150 },
    { src: "/images/vectors/town.png", width: 200 },
  ];
} else if (props.variable == 2) {
  images = [
    { src: "/images/vectors/21.png", width: 150 },
    { src: "/images/vectors/22.png", width: 200 },
    { src: "/images/vectors/23.png", width: 200 },
    { src: "/images/vectors/24.png", width: 200 },
    { src: "/images/vectors/21.png", width: 150 },
    { src: "/images/vectors/22.png", width: 200 },
  ];
} else {
  images = [
    { src: "/images/vectors/31.png", width: 150 },
    { src: "/images/vectors/32.png", width: 200 },
    { src: "/images/vectors/33.png", width: 200 },
    { src: "/images/vectors/34.png", width: 200 },
    { src: "/images/vectors/31.png", width: 150 },
    { src: "/images/vectors/32.png", width: 200 },
  ];
}

onMounted(() => {
  positions.value = initPositions(images);
});
</script>
