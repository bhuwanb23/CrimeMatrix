import { get, post } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function scoreSuspect(suspectId) {
  return post(`/suspect-risk/score/${suspectId}`)
}

export async function batchScoreSuspects() {
  return post('/suspect-risk/batch-score')
}

export async function getSuspectRiskScores(params = {}) {
  return get('/suspect-risk/scores' + toQuery(params))
}

export async function getSuspectRiskScore(suspectId) {
  return get(`/suspect-risk/scores/${suspectId}`)
}

export async function getSuspectRiskHistory(suspectId) {
  return get(`/suspect-risk/history/${suspectId}`)
}

export async function getSuspectRiskFactors(suspectId) {
  return get(`/suspect-risk/factors/${suspectId}`)
}

export async function getSuspectRiskRankings(limit = 10) {
  return get(`/suspect-risk/rankings?limit=${limit}`)
}

export async function getSuspectRiskStats() {
  return get('/suspect-risk/stats')
}
