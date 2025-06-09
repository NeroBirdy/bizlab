<template>
  <a href="/course">
    <img src="/assets/images/bizlap-logo.svg" alt="logo" class="bizlab-logo"
  /></a>
</template>

<script setup></script>

<style lang="scss" scoped>
a {
  margin-left: 5%;
  margin-top: 2%;
  display: block;
  width: max-content;
}

@media (max-width: 1110px) {
  a {
    margin-left: 20px;
  }
}

@media (max-width: 1024px) {
  a {
    margin-left: 10px;
  }
}

@media (max-width: 425px) {
  img {
    width: 50vw;
  }
}
</style>
