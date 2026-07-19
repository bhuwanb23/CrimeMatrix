import { get, post } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function detectHotspots() {
  return post('/hotspots/detect')
}

export async function listHotspots(filters = {}) {
  return get('/hotspots/' + toQuery(filters))
}

export async function getHotspot(id) {
  return get(`/hotspots/${id}`)
}

export async function getHotspotRankings(limit = 10) {
  return get(`/hotspots/rankings?limit=${limit}`)
}

export async function getRiskMap() {
  return get('/hotspots/risk-map')
}

export async function getClusters() {
  return get('/hotspots/clusters')
}

export async function getDensity(districtId) {
  return get(`/hotspots/density/${districtId}`)
}

export async function getHotspotStats() {
  return get('/hotspots/stats')
}
