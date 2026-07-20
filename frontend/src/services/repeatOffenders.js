import { get, post } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function listRepeatOffenders(filters = {}) {
  return get('/repeat-offenders/' + toQuery(filters))
}

export async function getRepeatOffender(id) {
  return get(`/repeat-offenders/${id}`)
}

export async function analyzeRepeatOffenders() {
  return post('/repeat-offenders/analyze')
}

export async function getRepeatOffenderRankings(limit = 10) {
  return get(`/repeat-offenders/rankings?limit=${limit}`)
}

export async function getRepeatOffenderStats() {
  return get('/repeat-offenders/stats')
}
