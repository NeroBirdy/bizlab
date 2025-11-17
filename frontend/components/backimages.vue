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
  margin-top: 5%;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

@media (max-width: 850px) {
  .background-vectors {
    display: none;
  }
}
</style>

<script setup>
import { ref, onMounted } from "vue";
import { initPositions } from "~/utils/shuffleback";

const positions = ref([]);

let images = [
  { src: "/images/vectors/yellow-rainbow.svg", width: 100, height: 100 },
  { src: "/images/vectors/blue-zigzag.svg", width: 100, height: 100 },
  { src: "/images/vectors/yellow-cup.svg", width: 100, height: 100 },
  { src: "/images/vectors/red-zigzag.svg", width: 100, height: 100 },
  { src: "/images/vectors/yellow-star.svg", width: 100, height: 100 },
  { src: "/images/vectors/red-bubna.svg", width: 100, height: 100 },
  { src: "/images/vectors/green-kaplya.svg", width: 100, height: 100 },
  { src: "/images/vectors/blue-sixgranik.svg", width: 100, height: 100 },
  { src: "/images/vectors/yellow-moon.svg", width: 100, height: 100 },
  { src: "/images/vectors/green-zigzag.svg", width: 100, height: 100 },
  { src: "/images/vectors/green-wave.svg", width: 100, height: 100 },
  { src: "/images/vectors/yellow-ranbow-left.svg", width: 100, height: 100 },
];

let lastWidth = window?.innerWidth || 0;
let lastHeight = window?.innerHeight || 0;

const resizeThreshold = 100;

onMounted(() => {
  if (!window) return;

  positions.value = initPositions(images);

  const handleResize = debounce(() => {
    const currentWidth = window.innerWidth;
    const currentHeight = window.innerHeight;

    const widthDiff = Math.abs(currentWidth - lastWidth);
    const heightDiff = Math.abs(currentHeight - lastHeight);

    if (widthDiff >= resizeThreshold || heightDiff >= resizeThreshold) {
      positions.value = initPositions(images);
      lastWidth = currentWidth;
      lastHeight = currentHeight;
    }
  }, 200);

  window.addEventListener("resize", handleResize);

  onUnmounted(() => {
    window.removeEventListener("resize", handleResize);
  });
});

function debounce(fn, delay) {
  let timeout;
  return () => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(), delay);
  };
}
</script>
