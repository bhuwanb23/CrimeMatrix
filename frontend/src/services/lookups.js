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

export async function seedLookups() {
  return post('/lookups/seed')
}
