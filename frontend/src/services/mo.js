import { get, post } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function getMOProfiles(crimeId = null) {
  return get('/mo/profiles' + toQuery({ crime_id: crimeId }))
}

export async function getMOProfile(profileId) {
  return get(`/mo/profiles/${profileId}`)
}

export async function createMOFingerprint(crimeId) {
  return post(`/mo/fingerprint/${crimeId}`)
}

export async function compareMOs(profileId1, profileId2) {
  return post('/mo/compare', { profile_id_1: profileId1, profile_id_2: profileId2 })
}

export async function findSimilarMOs(profileId, topK = 5) {
  return get(`/mo/similar/${profileId}?top_k=${topK}`)
}

export async function batchFingerprint() {
  return post('/mo/batch-fingerprint')
}

export async function getMOStats() {
  return get('/mo/stats')
}
