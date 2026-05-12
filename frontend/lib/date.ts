export function formatDate(value: string): string {
  return new Date(value).toLocaleDateString();
}

export function formatHours(value: number): string {
  return `${value.toFixed(2)} h`;
}
