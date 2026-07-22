import { get, post } from './api'

export async function analyzeFIR(firId) {
  return post(`/fir-intelligence/analyze/${firId}`)
}

export async function getFIRSuggestions(firId) {
  return get(`/fir-intelligence/suggestions/${firId}`)
}

export async function getFIRHistory(firId) {
  return get(`/fir-intelligence/history/${firId}`)
}

export async function getFIRIntelligenceStats() {
  return get('/fir-intelligence/stats')
}
