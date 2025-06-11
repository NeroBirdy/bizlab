<script setup>
const props = defineProps({
  bg: String,
  name: String,
  photo: String,
});
const bgImg = (await import(`@/assets/images/teachersPage/${props.bg}.png`))
  .default;
const maskImg = (
  await import(`@/assets/images/teachersPage/${props.bg}_clip.png`)
).default;
const imgSrc = (await import(`@/assets/images/teachersPage/${props.photo}.png`))
  .default;
</script>

<template>
  <div class="text-center teacher">
    <div
      :style="{
        backgroundImage: 'url(' + bgImg + ')',
        WebkitMaskImage: 'url(' + maskImg + ')',
        maskImage: 'url(' + maskImg + ')',
        maskSize: '100% 100%',
        maskRepeat: 'no-repeat',
      }"
      class="photo-card"
    >
      <img :src="imgSrc" class="clip-img" alt="Teacher avatar" />
    </div>
    <h2>{{ name }}</h2>
  </div>
</template>

<style  lang="scss" scoped>
.teacher {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 17.5vw;
}

.photo-card {
  position: relative;
  width: 14.8vw;
  min-height: 14.8vw;
  background-size: 100% 90%;
  background-position: bottom;
  background-repeat: no-repeat;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clip-img {
  position: absolute;
  bottom: 0;
  height: 100%;
  width: auto;
}

@media (max-width: 540px) {
  .photo-card {
    width: 35vw;
    min-height: 35vw;
  }
}
</style>
