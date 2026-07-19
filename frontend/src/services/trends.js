import { get, post } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function getTrendSummary(params = {}) {
  return get('/trends/summary' + toQuery(params))
}

export async function getDailyTrends(params = {}) {
  return get('/trends/daily' + toQuery(params))
}

export async function getWeeklyTrends(params = {}) {
  return get('/trends/weekly' + toQuery(params))
}

export async function getMonthlyTrends(params = {}) {
  return get('/trends/monthly' + toQuery(params))
}

export async function getYearlyTrends(params = {}) {
  return get('/trends/yearly' + toQuery(params))
}

export async function getDistrictTrends(districtId, days = 30) {
  return get(`/trends/district/${districtId}?days=${days}`)
}

export async function compareDistricts(ids, days = 30) {
  return get(`/trends/compare-districts?ids=${ids.join(',')}&days=${days}`)
}

export async function getSeasonalPatterns(days = 365) {
  return get(`/trends/seasonal?days=${days}`)
}

export async function getCrimeTypeTrends(days = 30) {
  return get(`/trends/crime-types?days=${days}`)
}

export async function getTrendSnapshots(metricName = null, limit = 30) {
  return get('/trends/snapshots' + toQuery({ metric_name: metricName, limit }))
}

export async function createTrendSnapshot(metricName, metricValue, comparisonValue = null) {
  return post('/trends/snapshots', { metric_name: metricName, metric_value: metricValue, comparison_value: comparisonValue })
}
