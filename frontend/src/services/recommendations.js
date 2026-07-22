import { get, post } from './api'

function toQuery(params) {
  const q = new URLSearchParams()
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') q.append(k, v)
  })
  return q.toString()
}

export async function getDashboardRecommendations() {
  return get('/recommendations/dashboard')
}

export async function getCaseRecommendations(caseId) {
  return get(`/recommendations/case/${caseId}`)
}

export async function getInvestigationRecommendations(investigationId) {
  return get(`/recommendations/investigation/${investigationId}`)
}

export async function naturalLanguageSearch(query) {
  return post('/recommendations/search/natural-language', { query })
}

export async function getAllRecommendations(params = {}) {
  const query = toQuery(params)
  return get('/recommendations/all' + (query ? `?${query}` : ''))
}

export async function submitFeedback(recommendationId, feedback) {
  return post(`/recommendations/${recommendationId}/feedback`, { feedback })
}

export async function getRecommendationHistory(params = {}) {
  const query = toQuery(params)
  return get('/recommendations/history' + (query ? `?${query}` : ''))
}

export async function generateRecommendations(contextType = 'dashboard', entityId = null) {
  const params = { context_type: contextType }
  if (entityId) params.entity_id = entityId
  const query = toQuery(params)
  return post(`/recommendations/generate?${query}`)
}
