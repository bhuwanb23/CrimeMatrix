import { get, post } from './api'

export async function analyzeInvestigation(investigationId, analysisType = 'summary', question = null) {
  const payload = { analysis_type: analysisType }
  if (question) payload.question = question
  return post(`/investigations/${investigationId}/analyze`, payload)
}

export async function askInvestigationQuestion(investigationId, question) {
  return post('/ai/chat', {
    message: `Regarding investigation #${investigationId}: ${question}`,
    use_tools: true,
  })
}

export async function getInvestigationInsights(investigationId) {
  return get(`/investigations/${investigationId}/analyze?analysis_type=summary`)
}
