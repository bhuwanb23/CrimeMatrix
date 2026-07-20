import { get, post, put } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function listAlerts(params = {}) {
  return get('/early-warning/alerts' + toQuery(params))
}

export async function getAlert(id) {
  return get(`/early-warning/alerts/${id}`)
}

export async function acknowledgeAlert(id, acknowledgedBy = 'Officer') {
  return put(`/early-warning/alerts/${id}/acknowledge`, { acknowledged_by: acknowledgedBy })
}

export async function detectAlerts() {
  return post('/early-warning/detect')
}

export async function listAlertRules() {
  return get('/early-warning/rules')
}

export async function createAlertRule(data) {
  return post('/early-warning/rules', data)
}

export async function getAlertTimeline(days = 30) {
  return get(`/early-warning/timeline?days=${days}`)
}

export async function getEarlyWarningStats() {
  return get('/early-warning/stats')
}
