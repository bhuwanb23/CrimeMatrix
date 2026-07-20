import { get, post } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function generateForecast(params = {}) {
  return post('/predictions/forecast', params)
}

export async function listPredictions(params = {}) {
  return get('/predictions/' + toQuery(params))
}

export async function getPrediction(id) {
  return get(`/predictions/${id}`)
}

export async function getDistrictPredictions(districtId) {
  return get(`/predictions/district/${districtId}`)
}

export async function getPredictionModels() {
  return get('/predictions/models')
}

export async function getPredictionStats() {
  return get('/predictions/stats')
}
