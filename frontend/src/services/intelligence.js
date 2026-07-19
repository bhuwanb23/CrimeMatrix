import { get } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function getIntelligenceSummary(params = {}) {
  return get('/intelligence/summary' + toQuery(params))
}

export async function getIntelligenceTrends(timeRange = '30d') {
  return get(`/intelligence/trends?time_range=${timeRange}`)
}

export async function getIntelligenceHotspots(timeRange = '30d') {
  return get(`/intelligence/hotspots?time_range=${timeRange}`)
}
