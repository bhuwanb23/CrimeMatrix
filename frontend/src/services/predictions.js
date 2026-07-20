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

export async function forecastDistrict(districtId, periods = 30) {
  return post('/predictions/forecast/district', { district_id: districtId, periods })
}

export async function forecastCategory(crimeTypeId, periods = 30) {
  return post('/predictions/forecast/category', { crime_type_id: crimeTypeId, periods })
}

export async function getSeasonalPatterns(days = 365) {
  return get(`/predictions/forecast/seasonal?days=${days}`)
}

export async function getForecastHistory(limit = 30) {
  return get(`/predictions/forecast/history?limit=${limit}`)
}

export async function getForecastStats() {
  return get('/predictions/forecast/stats')
}

export async function explainPrediction(predictionId) {
  return post(`/predictions/explain/${predictionId}`)
}

export async function getPredictionExplanation(predictionId) {
  return get(`/predictions/explain/${predictionId}`)
}

export async function getPredictionSources(predictionId) {
  return get(`/predictions/sources/${predictionId}`)
}

export async function getPredictionConfidence(predictionId) {
  return get(`/predictions/confidence/${predictionId}`)
}
