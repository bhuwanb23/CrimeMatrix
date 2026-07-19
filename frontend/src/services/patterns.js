import { get, post } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function detectPatterns() {
  return post('/patterns/detect')
}

export async function listPatterns(filters = {}) {
  return get('/patterns/' + toQuery(filters))
}

export async function getPattern(id) {
  return get(`/patterns/${id}`)
}

export async function getPatternOccurrences(id) {
  return get(`/patterns/${id}/occurrences`)
}

export async function getClusters() {
  return get('/patterns/clusters')
}

export async function comparePatterns(id1, id2) {
  return get(`/patterns/compare/${id1}/${id2}`)
}

export async function getPatternStats() {
  return get('/patterns/stats')
}
