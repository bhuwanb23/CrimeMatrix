import { get, post } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function getBehaviorProfiles(criminalId = null) {
  return get('/behavior/profiles' + toQuery({ criminal_id: criminalId }))
}

export async function analyzeCriminal(criminalId) {
  return post(`/behavior/analyze/${criminalId}`)
}

export async function getRiskAssessment() {
  return get('/behavior/risk-assessment')
}

export async function getBehaviorFeatures(profileId) {
  return get(`/behavior/features/${profileId}`)
}

export async function getBehaviorStats() {
  return get('/behavior/stats')
}
