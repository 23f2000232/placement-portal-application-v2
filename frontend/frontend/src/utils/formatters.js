export function formatDate(date, fallback = '-') {
  if (!date) {
    return fallback
  }

  return new Date(date).toLocaleDateString()
}

export function toLocalDateTimeInput(value) {
  const date = new Date(value)
  const pad = (number) => String(number).padStart(2, '0')

  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

export function formatEnum(value) {
  return value
    .replaceAll('_', ' ')
    .toLowerCase()
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

export function formatExperience(years) {
  if (years === 0) {
    return 'Freshers'
  }

  return `${years} Years`
}
