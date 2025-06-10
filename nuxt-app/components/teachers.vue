<template>
  <div class="teacherContent">
    <h1 class="text-center">наша команда</h1>
    <h5 class="text-center">Люди, которые знают своё дело</h5>
    <!-- <img
      src="/assets/images/teachersPage/vectorStar.svg"
      alt="Star"
      class="star"
    />
    <img
      src="/images/vectors/green-kaplya.svg"
      alt="Wave"
      class="wave"
    /> -->
    <div class="teachersCard">
      <teacher name="Кристина" bg="red" photo="photo"/>
      <teacher name="Кристина" bg="blue" photo="photo"/>
      <teacher name="Кристина" bg="yellow" photo="photo"/>
    </div>
  </div>
</template>

<style lang="scss" scooped>
.teacherContent {
  width: 100vw;
  height: 90vh;
}

.teachersCard {
  margin-top: 7vw;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
  gap: 3vw;
  width: 80%;
  margin-left: auto;
  margin-right: auto;

  grid-template-areas:
    "teacher teacher"
    "teacher .";
}

.star,
.wave {
  position: absolute;
  z-index: -1;
}

.star {
  top: 0;
  left: 0;
  scale: 0.8;
}

.wave {
  top: 25%;
  right: -15vw;
  scale: 0.3;
}
@media (max-width: 1025px) {
  .wave {
    top: 25%;
    right: -25vw;
    scale: 0.3;
  }
}

@media (max-width: 767px) {
  .star {
    left: -10vw;
    scale: 0.5;
  }
  .wave {
    top: 30%;
    right: -30vw;
  }
}

@media (max-width: 1160px) and (min-width: 730px) {
  .teachersCard div:nth-child(3) {
    grid-column: 1 / span 2;
    grid-row: 2 / 3;
  }
}

</style>
