<template>
  <div class="relative w-full justify-center flex">
    <div class="ml-auto mr-auto">
      <h1 class="text-center">ОТЗЫВЫ НАШИХ клиентов</h1>
      <div class="cards">
        <Review
          color="#F0AC02"
          name="Татьяна Шелковицина"
          review="С учебным центром «BIZLAB» сотрудничаем более 6 лет.
Прекрасные преподаватели, внимательный персонал. Хорошие
программы для больших и маленьких."
        />
        <Review
          color="blue"
          name="Татьяна Шелковицина"
          review="Всем привет всем пока какиккак"
        />
        <Review
          color="#E25D35"
          name="Татьяна Шелковицина"
          review="Всем привет всем пока какиккак"
        />
      </div>
    </div>
    <img
      src="/assets/images/reviewsPage/l-line.svg"
      alt=""
      class="line left-0"
    />
    <img
      src="/assets/images/reviewsPage/r-line.svg"
      alt=""
      class="line right-0"
    />
  </div>
</template>

<style lang="scss" scoped>
.cards {
  display: flex;
  column-gap: 93px;
  margin-top: 50px;
}

.line {
  position: absolute;
  z-index: 2;
  bottom: -130px;
}
</style>
