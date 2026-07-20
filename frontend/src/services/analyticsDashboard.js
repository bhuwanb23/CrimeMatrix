import { get } from './api'

export async function getDashboardSummary() {
  return get('/analytics-dashboard/summary')
}

export async function getDashboardAlerts() {
  return get('/analytics-dashboard/alerts')
}

export async function getDashboardForecasts() {
  return get('/analytics-dashboard/forecasts')
}

export async function getDashboardHighRisk() {
  return get('/analytics-dashboard/high-risk')
}

export async function getDashboardPriority() {
  return get('/analytics-dashboard/priority')
}

export async function getDashboardStats() {
  return get('/analytics-dashboard/stats')
}
