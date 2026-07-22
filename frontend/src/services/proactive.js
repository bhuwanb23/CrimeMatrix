import { get, post } from './api'

export async function getProactiveStats() {
  return get('/proactive/stats')
}

export async function listEvents(params = {}) {
  return get('/proactive/events' + toQuery(params))
}

export async function getEvent(id) {
  return get(`/proactive/events/${id}`)
}

export async function createEvent(data) {
  return post('/proactive/events', data)
}

export async function processEvents() {
  return post('/proactive/events/process')
}

export async function scanData() {
  return post('/proactive/scan')
}

export async function getEventQueue() {
  return get('/proactive/queue')
}

export async function getProcessed(limit = 20) {
  return get(`/proactive/processed?limit=${limit}`)
}

export async function getActivity(limit = 20) {
  return get(`/proactive/activity?limit=${limit}`)
}

export async function batchProcess() {
  return post('/proactive/batch-process')
}

export async function explainEvent(eventId) {
  return post(`/proactive/explain/event/${eventId}`)
}

export async function explainRecommendation(recId) {
  return post(`/proactive/explain/recommendation/${recId}`)
}

export async function explainEvidenceLink(linkId) {
  return post(`/proactive/explain/evidence-link/${linkId}`)
}

export async function explainAlert(alertId) {
  return post(`/proactive/explain/alert/${alertId}`)
}

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}
