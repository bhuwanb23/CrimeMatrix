import { get, post, put, del } from './api';

function toQuery(params) {
  const qs = Object.entries(params)
    .filter(([, v]) => v !== undefined && v !== null && v !== '')
    .map(([k, v]) => `${k}=${encodeURIComponent(v)}`)
    .join('&');
  return qs ? `?${qs}` : '';
}

// Investigations
export async function listInvestigations(filters = {}) {
  return get('/investigations/' + toQuery(filters));
}

export async function getInvestigation(id) {
  return get(`/investigations/${id}`);
}

export async function createInvestigation(data) {
  return post('/investigations/', data);
}

export async function updateInvestigation(id, data) {
  return put(`/investigations/${id}`, data);
}

export async function deleteInvestigation(id) {
  return del(`/investigations/${id}`);
}

export async function getRecentInvestigations(limit = 3) {
  return get(`/investigations/recent?limit=${limit}`);
}

export async function toggleSaveInvestigation(id) {
  return put(`/investigations/${id}/save`);
}

export async function getInvestigationStats() {
  return get('/investigations/stats');
}

// Notes
export async function listNotes(investigationId) {
  return get(`/notes/investigation/${investigationId}`);
}

export async function createNote(data) {
  return post('/notes/', data);
}

export async function deleteNote(id) {
  return del(`/notes/${id}`);
}

// Timeline
export async function listTimelineEvents(investigationId) {
  return get(`/timeline/investigation/${investigationId}`);
}

export async function createTimelineEvent(data) {
  return post('/timeline/', data);
}

export async function deleteTimelineEvent(id) {
  return del(`/timeline/${id}`);
}

// Case Links
export async function listCaseLinks(investigationId) {
  return get(`/case-links/investigation/${investigationId}`);
}

export async function createCaseLink(data) {
  return post('/case-links/', data);
}

export async function deleteCaseLink(id) {
  return del(`/case-links/${id}`);
}

// Status Logs
export async function listStatusLogs(investigationId) {
  return get(`/case-status/investigation/${investigationId}`);
}

export async function createStatusLog(data) {
  return post('/case-status/', data);
}

// Attachments
export async function listAttachments(investigationId) {
  return get(`/attachments/investigation/${investigationId}`);
}

export async function uploadAttachment(investigationId, file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('investigation_id', investigationId);
  const base = import.meta.env.VITE_API_URL || 'http://localhost:8001/api/v1';
  const res = await fetch(`${base}/attachments/upload`, {
    method: 'POST',
    body: formData,
  });
  return res.json();
}

export async function deleteAttachment(id) {
  return del(`/attachments/${id}`);
}

// Bookmarks — prefer frontend/src/services/bookmarks.js; these re-export for compatibility
export {
  listBookmarks,
  createBookmark,
  removeBookmark as deleteBookmark,
} from './bookmarks'
