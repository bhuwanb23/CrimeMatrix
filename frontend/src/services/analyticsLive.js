import { get } from './api'

export async function getStatistics() {
  return get('/statistics')
}

export async function getAnalyticsOverview() {
  return get('/analytics/stats/overview')
}

export async function getAnalyticsSummary() {
  return get('/analytics/stats/summary')
}

export async function getCrimeTrends(params = '') {
  return get('/analytics/trends/crimes' + (params ? `?${params}` : ''))
}

export async function getCaseTrends(params = '') {
  return get('/analytics/trends/cases' + (params ? `?${params}` : ''))
}

export async function getResolutionTrends() {
  return get('/analytics/trends/resolution')
}

export async function getCountsByType() {
  return get('/analytics/counts/by-type')
}

export async function getCountsByStatus() {
  return get('/analytics/counts/by-status')
}

export async function getCountsByDistrict() {
  return get('/analytics/counts/by-district')
}

export async function getCountsByPriority() {
  return get('/analytics/counts/by-priority')
}

export async function getCrimeTimeseries(params = '') {
  return get('/analytics/timeseries/crimes' + (params ? `?${params}` : ''))
}

export async function getCaseTimeseries(params = '') {
  return get('/analytics/timeseries/cases' + (params ? `?${params}` : ''))
}

export async function getActivityTimeseries(params = '') {
  return get('/analytics/timeseries/activity' + (params ? `?${params}` : ''))
}

export async function getDistrictAnalytics() {
  return get('/analytics/districts')
}
