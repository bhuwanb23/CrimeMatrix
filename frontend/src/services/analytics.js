import { get, post } from './api'

export async function getEvaluationStats() {
  return get('/evaluation/stats')
}

export async function runEvaluation() {
  return post('/evaluation/run')
}

export async function getEvaluationResults() {
  return get('/evaluation/results')
}

export async function getAccuracyTrend() {
  return get('/evaluation/accuracy-trend')
}

export async function getEvaluationFeedback(predictionId = null) {
  const qs = predictionId ? `?prediction_id=${predictionId}` : ''
  return get('/evaluation/feedback' + qs)
}

export async function submitFeedback(data) {
  return post('/evaluation/feedback', data)
}

export async function getDrift() {
  return get('/evaluation/drift')
}
