/** Keep first occurrence of each value for `key` (e.g. duplicate API rows). */
export function dedupeByKey(items, key = 'id') {
  if (!Array.isArray(items)) return []
  const seen = new Set()
  return items.filter((item) => {
    const value = item?.[key]
    if (value === undefined || value === null) return true
    const token = String(value)
    if (seen.has(token)) return false
    seen.add(token)
    return true
  })
}
