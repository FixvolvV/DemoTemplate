// ===== КАПЧА — КЛИЕНТСКАЯ ЛОГИКА =====
// Одна картинка разрезана на 4 части (сетка 2x2)
// Части пронумерованы:
//   1 | 2
//   -----
//   3 | 4
// Пользователь должен собрать картинку, переставляя куски

export const CAPTCHA_IMAGES = [
  '/captcha/1.svg',  // верх-лево     Замени на .png если нужно
  '/captcha/2.svg',  // верх-право
  '/captcha/3.svg',  // низ-лево
  '/captcha/4.svg',  // низ-право
]

export interface CaptchaData {
  // Перемешанные индексы (какая картинка стоит на какой позиции)
  // Например [3, 1, 4, 2] значит: на позиции 0 стоит кусок 3, на позиции 1 — кусок 1, ...
  slots: number[]
}

// Перемешать массив (Fisher-Yates)
function shuffle<T>(array: T[]): T[] {
  const arr = [...array]
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }
  // Если не перемешалось (совпал порядок) — перемешиваем ещё раз
  if (arr.every((v, i) => v === array[i])) return shuffle(array)
  return arr
}

// Генерация: перемешиваем куски
export function generateCaptcha(): CaptchaData {
  const slots = shuffle([1, 2, 3, 4])
  return { slots }
}

// Проверка: каждый кусок на своём месте
export function verifyCaptcha(slots: number[]): boolean {
  return slots[0] === 1 && slots[1] === 2 && slots[2] === 3 && slots[3] === 4
}

// Путь к картинке по номеру куска
export function getImageSrc(pieceNumber: number): string {
  return CAPTCHA_IMAGES[pieceNumber - 1]
}
