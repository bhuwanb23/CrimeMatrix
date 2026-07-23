import { get, post } from './api'

export async function getCategories() {
  return get('/lookups/categories')
}

export async function getGravityOffences() {
  return get('/lookups/gravity-offences')
}

export async function getCrimeHeads() {
  return get('/lookups/crime-heads')
}

export async function getCrimeSubHeads(crimeHeadId = null) {
  const params = crimeHeadId ? `?crime_head_id=${crimeHeadId}` : ''
  return get('/lookups/crime-sub-heads' + params)
}

export async function getCaseStatuses() {
  return get('/lookups/case-statuses')
}

export async function getCourts() {
  return get('/lookups/courts')
}

export async function getOccupations() {
  return get('/lookups/occupations')
}

export async function getReligions() {
  return get('/lookups/religions')
}

export async function getCaste() {
  return get('/lookups/caste')
}

export async function getGenders() {
  return get('/lookups/genders')
}

export async function getComplainant(caseId) {
  return get(`/cases/${caseId}/complainant`)
}

export async function createComplainant(caseId, data) {
  return post(`/cases/${caseId}/complainant`, data)
}

export async function seedLookups() {
  return post('/lookups/seed')
}
