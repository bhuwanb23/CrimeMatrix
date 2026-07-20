import { get, post } from './api'

export async function scoreInvestigation(investigationId) {
  return post(`/priorities/score/${investigationId}`)
}

export async function batchScorePriorities() {
  return post('/priorities/batch-score')
}

export async function listPriorities(params = {}) {
  const qs = Object.entries(params).filter(([, v]) => v != null).map(([k, v]) => `${k}=${v}`).join('&')
  return get('/priorities/' + (qs ? `?${qs}` : ''))
}

export async function getPriorityExplain(investigationId) {
  return get(`/priorities/explain/${investigationId}`)
}

export async function getPriorityRankings(limit = 10) {
  return get(`/priorities/rankings?limit=${limit}`)
}

export async function getPriorityHistory(investigationId) {
  return get(`/priorities/history/${investigationId}`)
}

export async function getWorkload() {
  return get('/priorities/workload')
}

export async function getPriorityStats() {
  return get('/priorities/stats')
}
