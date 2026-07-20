import { get } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function getFullTimeline(params = {}) {
  return get('/criminal-timeline/' + toQuery(params))
}

export async function getSuspectTimeline(suspectName, days = 90) {
  return get(`/criminal-timeline/suspect/${encodeURIComponent(suspectName)}?days=${days}`)
}

export async function getInvestigationTimeline(investigationId) {
  return get(`/criminal-timeline/investigation/${investigationId}`)
}

export async function getTimelineStats() {
  return get('/criminal-timeline/stats')
}
