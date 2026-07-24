import { get, post, del } from './api'

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&')
  return qs ? `?${qs}` : ''
}

// Nodes
export async function getGraphNodes(params = {}) {
  return get('/graph/nodes' + toQuery(params))
}

export async function getGraphNode(nodeId) {
  return get(`/graph/nodes/${nodeId}`)
}

export async function createGraphNode(data) {
  return post('/graph/nodes', data)
}

export async function deleteGraphNode(nodeId) {
  return del(`/graph/nodes/${nodeId}`)
}

// Edges
export async function getGraphEdges(params = {}) {
  return get('/graph/edges' + toQuery(params))
}

export async function createGraphEdge(data) {
  return post('/graph/edges', data)
}

export async function deleteGraphEdge(source, target) {
  return del(`/graph/edges/${source}/${target}`)
}

// Traversal
export async function traverseGraph(startNode, method = 'bfs', maxDepth = 3) {
  return get(`/graph/traverse/${encodeURIComponent(startNode)}?method=${encodeURIComponent(method)}&max_depth=${maxDepth}`)
}

export async function shortestPath(source, target) {
  return get(`/graph/shortest/${encodeURIComponent(source)}/${encodeURIComponent(target)}`)
}

export async function getNeighbors(nodeId, edgeType = null) {
  return get(`/graph/neighbors/${nodeId}` + toQuery({ edge_type: edgeType }))
}

// Stats & Components
export async function getGraphStats() {
  return get('/graph/stats')
}

export async function getGraphComponents() {
  return get('/graph/components')
}

// Build from crimes
export async function buildGraphFromCrimes() {
  return post('/graph/build-from-crimes')
}

// Load/Save
export async function loadGraph() {
  return post('/graph/load')
}

export async function saveGraph() {
  return post('/graph/save')
}
