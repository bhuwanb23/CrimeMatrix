import { get, post, del } from './api'

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

export async function getActs() {
  return get('/lookups/acts')
}

export async function getSections(actId = null) {
  const params = actId ? `?act_id=${actId}` : ''
  return get('/lookups/sections' + params)
}

export async function getActSections(caseId) {
  return get(`/cases/${caseId}/act-sections`)
}

export async function getCrimeHeadActSections(crimeHeadId = null) {
  const params = crimeHeadId ? `?crime_head_id=${crimeHeadId}` : ''
  return get('/lookups/crime-head-act-sections' + params)
}

export async function addActSection(caseId, data) {
  return post(`/cases/${caseId}/act-sections`, data)
}

export async function deleteActSection(caseId, assocId) {
  return del(`/cases/${caseId}/act-sections/${assocId}`)
}

export async function getVictims(caseId) {
  return get(`/cases/${caseId}/victims`)
}

export async function createVictim(caseId, data) {
  return post(`/cases/${caseId}/victims`, data)
}

export async function updateVictim(caseId, victimId, data) {
  return post(`/cases/${caseId}/victims/${victimId}`, data)
}

export async function deleteVictim(caseId, victimId) {
  return del(`/cases/${caseId}/victims/${victimId}`)
}

export async function getStates() {
  return get('/lookups/states')
}

export async function getArrestSurrenderTypes() {
  return get('/lookups/arrest-surrender-types')
}

export async function getAccused(caseId) {
  return get(`/cases/${caseId}/accused`)
}

export async function createAccused(caseId, data) {
  return post(`/cases/${caseId}/accused`, data)
}

export async function updateAccused(caseId, accusedId, data) {
  return post(`/cases/${caseId}/accused/${accusedId}`, data)
}

export async function deleteAccused(caseId, accusedId) {
  return del(`/cases/${caseId}/accused/${accusedId}`)
}

export async function getArrestSurrender(caseId) {
  return get(`/cases/${caseId}/arrest-surrender`)
}

export async function createArrestSurrender(caseId, data) {
  return post(`/cases/${caseId}/arrest-surrender`, data)
}

export async function updateArrestSurrender(caseId, recordId, data) {
  return post(`/cases/${caseId}/arrest-surrender/${recordId}`, data)
}

export async function deleteArrestSurrender(caseId, recordId) {
  return del(`/cases/${caseId}/arrest-surrender/${recordId}`)
}

export async function getUnitTypes() {
  return get('/lookups/unit-types')
}

export async function getRanks() {
  return get('/lookups/ranks')
}

export async function seedLookups() {
  return post('/lookups/seed')
}
