import { get, post } from './api'

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
