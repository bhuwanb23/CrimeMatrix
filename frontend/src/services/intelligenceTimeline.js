import { get } from './api'

function toQuery(params) {
  const q = new URLSearchParams()
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') q.append(k, v)
  })
  return q.toString()
}

export async function getUnifiedTimeline(params = {}) {
  const query = toQuery(params)
  return get('/intelligence-timeline/' + (query ? `?${query}` : ''))
}

export async function getEventHistory(params = {}) {
  const query = toQuery(params)
  return get('/intelligence-timeline/events' + (query ? `?${query}` : ''))
}

export async function getAlertHistory(params = {}) {
  const query = toQuery(params)
  return get('/intelligence-timeline/alerts' + (query ? `?${query}` : ''))
}

export async function getEvidenceHistory(params = {}) {
  const query = toQuery(params)
  return get('/intelligence-timeline/evidence' + (query ? `?${query}` : ''))
}

export async function getRecommendationHistoryTimeline(params = {}) {
  const query = toQuery(params)
  return get('/intelligence-timeline/recommendations' + (query ? `?${query}` : ''))
}

export async function getRiskHistory(params = {}) {
  const query = toQuery(params)
  return get('/intelligence-timeline/risk' + (query ? `?${query}` : ''))
}

export async function getTimelineStats() {
  return get('/intelligence-timeline/stats')
}
