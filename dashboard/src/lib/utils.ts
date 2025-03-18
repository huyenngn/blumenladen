function formatCurrency(value: number) {
  return (value / 100).toLocaleString('de-DE', { style: 'currency', currency: 'EUR' })
}

function formatPercentage(value: number) {
  return value + '%'
}

function formatDate(value: string): string {
  const date = new Date(value)
  return date.toLocaleDateString('de-DE', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  })
}

function formatDateTime(value: string): string {
  const date = new Date(value)
  return date.toLocaleDateString('de-DE', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function formatMonthShort(value: string): string {
  const date = new Date(value)
  return date.toLocaleDateString('de-DE', {
    month: 'short',
  })
}

function formatMonth(value: string): string {
  const date = new Date(value)
  return date.toLocaleDateString('de-DE', {
    month: 'long',
    year: 'numeric',
  })
}

export {
  formatCurrency,
  formatDate,
  formatDateTime,
  formatMonth,
  formatMonthShort,
  formatPercentage,
}
