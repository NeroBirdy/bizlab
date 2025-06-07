function getRandomPosition(maxX, maxY) {
  const x = Math.random() * maxX;
  const y = Math.random() * maxY;
  return { x, y };
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function isOverlapping(rect1, rect2) {
  return !(
    rect1.x + rect1.width < rect2.x ||
    rect2.x + rect2.width < rect1.x ||
    rect1.y + rect1.height < rect2.y ||
    rect2.y + rect2.height < rect1.y
  );
}

export function initPositions(images) {
  const windowSize = ref({ width: 0, height: 0 });
  const { innerWidth: width, innerHeight: height } = window;
  windowSize.value = { width, height };

  const positioned = [];
  const attemptsLimit = 100;

  shuffleArray(images);

  for (const img of images) {
    let x, y;
    let attempts = 0;
    let collision = false;

    do {
      // Генерируем случайные x и y
      x = Math.random() * (width - img.width);
      y = Math.random() * (height - img.width);

      collision = positioned.some((pos) =>
        isOverlapping(
          { x, y, width: img.width, height: img.height },
          { x: pos.x, y: pos.y, width: pos.width, height: pos.height }
        )
      );

      attempts++;
    } while (collision && attempts < attemptsLimit);

    if (attempts < attemptsLimit) {
      positioned.push({
        src: img.src,
        width: img.width,
        height: img.height,
        x,
        y,
      });
    } else {
      console.warn("Не удалось разместить изображение без пересечения:", img);
    }
  }

  return positioned;
}
