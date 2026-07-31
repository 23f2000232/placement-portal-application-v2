export function formatDate(date, fallback = '-') {
  if (!date) {
    return fallback
  }

  return new Date(date).toLocaleDateString()
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
