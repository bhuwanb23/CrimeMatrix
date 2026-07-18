import { get, post, put, del, stream } from './api';

export async function chat(message, sessionId, userId = 'default', useTools = true, language = 'en') {
    return post('/copilot/chat', { message, session_id: sessionId, user_id: userId, use_tools: useTools, language });
}

export function chatStream(message, sessionId, userId = 'default', language = 'en', onChunk, onDone) {
    return stream('/copilot/chat/stream', { message, session_id: sessionId, user_id: userId, use_tools: true, language }, onChunk, onDone);
}

export async function listSessions(userId = 'default') {
    return get(`/copilot/sessions?user_id=${userId}`);
}

export async function createSession(title) {
    return post('/copilot/sessions', { title });
}

export async function getSession(sessionId) {
    return get(`/copilot/sessions/${sessionId}`);
}

export async function deleteSession(sessionId) {
    return del(`/copilot/sessions/${sessionId}`);
}

export async function updateSessionTitle(sessionId, title) {
    return put(`/copilot/sessions/${sessionId}/title`, { title });
}

export async function deleteAllSessions() {
    return del('/copilot/sessions');
}

export async function togglePin(sessionId) {
    return put(`/copilot/sessions/${sessionId}/pin`);
}

export async function searchSessions(query) {
    return get(`/copilot/sessions/search?q=${encodeURIComponent(query)}`);
}

export async function exportSession(sessionId) {
    return get(`/copilot/sessions/${sessionId}/export`);
}

export async function bookmarkMessage(sessionId, content, role = 'assistant', note = '') {
    return post('/copilot/bookmarks', { session_id: sessionId, message_content: content, message_role: role, note });
}

export async function listBookmarks(sessionId) {
    return get(`/copilot/bookmarks${sessionId ? '?session_id=' + sessionId : ''}`);
}

export async function deleteBookmark(bookmarkId) {
    return del(`/copilot/bookmarks/${bookmarkId}`);
}
