import { get } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

export async function getCrimeMarkers(params = {}) {
  return get('/maps/crime-markers' + toQuery(params))
}

export async function getDistrictGeoJSON() {
  return get('/maps/districts')
}

export async function getHeatmapData(days = 30) {
  return get(`/maps/heatmap?days=${days}`)
}

export async function getHotspotMarkers() {
  return get('/maps/hotspots')
}

export async function getStationMarkers() {
  return get('/maps/stations')
}

export async function getRouteData() {
  return get('/maps/routes')
}

export async function getMapStats() {
  return get('/maps/stats')
}
