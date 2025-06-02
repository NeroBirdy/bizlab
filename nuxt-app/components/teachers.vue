<template>
  <div class="w-full flex-row justify-center relative">
    <h1 class="text-center">наша команда</h1>
    <h5 class="text-center">Люди, которые знают своё дело</h5>
    <img
      src="/assets/images/teachersPage/vectorStar.svg"
      alt="Star"
      class="star"
    />
    <img
      src="/assets/images/teachersPage/vectorWave.svg"
      alt="Wave"
      class="wave"
    />
    <div class="teachersCard">
      <teacher name="Кристина" bg="red" photo="photo" />
      <teacher name="Кристина" bg="blue" photo="photo" />
      <teacher name="Кристина" bg="yellow" photo="photo" />
    </div>
  </div>
</template>

<style lang="scss" scooped>
.teachersCard {
  margin-top: 100px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 55%;
  margin-left: auto;
  margin-right: auto;
}

.star,
.wave {
  position: absolute;
  z-index: -1;
}

.star {
  top: 0;
  left: 0;
}

.wave {
  right: 0;
  top: -30%;
}
</style>
