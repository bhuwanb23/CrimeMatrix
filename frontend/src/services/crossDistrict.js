import { get, post } from './api'

export async function detectCrossDistrict() {
  return post('/cross-district/detect')
}

export async function listCrossDistrictMatches(matchType = null) {
  return get('/cross-district/matches' + toQuery({ match_type: matchType }))
}

export async function getCrossDistrictMatch(id) {
  return get(`/cross-district/matches/${id}`)
}

export async function compareCrossDistrict(district1, district2) {
  return get(`/cross-district/compare?district1=${district1}&district2=${district2}`)
}

export async function getCrossDistrictStats() {
  return get('/cross-district/stats')
}

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}
