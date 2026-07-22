import { get, post } from './api'

export async function detectEvidenceLinks() {
  return post('/evidence-linking/detect')
}

export async function listEvidenceLinks(linkType = null) {
  return get('/evidence-linking/links' + toQuery({ link_type: linkType }))
}

export async function getEvidenceLink(id) {
  return get(`/evidence-linking/links/${id}`)
}

export async function getEvidenceRelationships() {
  return get('/evidence-linking/relationships')
}

export async function getEvidenceLinkingStats() {
  return get('/evidence-linking/stats')
}

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}
