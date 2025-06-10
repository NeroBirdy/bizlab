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
  const { innerWidth: width, innerHeight: height } = window;
  const positioned = [];
  const attemptsLimit = 1000; // Разумное число попыток на объект
  const minDistance = 150; // Увеличенное минимальное расстояние между центрами объектов

  // Зоны по бокам
  const sideWidth = width * 0.2;
  const leftZone = { x: 0, width: sideWidth };
  const rightZone = { x: width - sideWidth, width: sideWidth };

  // Делим картинки строго пополам
  const half = Math.ceil(images.length / 2);
  const leftImages = images.slice(0, half);
  const rightImages = images.slice(half);

  // Функция для генерации позиции внутри заданной зоны
  function tryPlaceImage(zone, img, others) {
    let attempts = 0;

    while (attempts < attemptsLimit) {
      const x = zone.x + Math.random() * (zone.width - img.width);
      const y = Math.random() * (height - img.height); // Случайная вертикальная позиция

      const collision = others.some((pos) => {
        const dx = Math.abs(x + img.width / 2 - (pos.x + pos.width / 2));
        const dy = Math.abs(y + img.height / 2 - (pos.y + pos.height / 2));
        const distance = Math.sqrt(dx * dx + dy * dy);
        return (
          distance < minDistance ||
          isOverlapping(
            { x, y, width: img.width, height: img.height },
            { x: pos.x, y: pos.y, width: pos.width, height: pos.height }
          )
        );
      });

      if (!collision) {
        return { ...img, x, y };
      }

      attempts++;
    }

    // Если не нашли место, всё равно пытаемся положить без проверки
    const x = zone.x + Math.random() * (zone.width - img.width);
    const y = Math.random() * (height - img.height);
    return { ...img, x, y };
  }

  // Размещаем сначала левые
  const placedLeft = [];
  for (let i = 0; i < leftImages.length; i++) {
    const img = leftImages[i];
    const placed = tryPlaceImage(leftZone, img, placedLeft);
    placedLeft.push(placed);
  }

  // Размещаем правые
  const placedRight = [];
  for (let i = 0; i < rightImages.length; i++) {
    const img = rightImages[i];
    const placed = tryPlaceImage(rightZone, img, placedRight);
    placedRight.push(placed);
  }

  return [...placedLeft, ...placedRight];
}