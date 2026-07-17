import { get, post, put, del, stream } from './api';

export async function chat(message, sessionId, userId = 'default', useTools = true) {
    return post('/copilot/chat', {
        message,
        session_id: sessionId,
        user_id: userId,
        use_tools: useTools,
    });
}

export function chatStream(message, sessionId, userId = 'default', onChunk, onDone) {
    return stream('/copilot/chat/stream', {
        message,
        session_id: sessionId,
        user_id: userId,
        use_tools: true,
    }, onChunk, onDone);
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
