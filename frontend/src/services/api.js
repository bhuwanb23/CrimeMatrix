const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

async function apiRequest(path, options = {}) {
    const url = `${API_BASE}${path}`;
    const method = (options.method || 'GET').toUpperCase();
    const headers = { ...(options.headers || {}) };
    // Avoid Content-Type on body-less requests so GETs stay "simple" and skip CORS preflight
    // (AppSail edge OPTIONS often omits ACAO until the Slate origin is whitelisted).
    if (options.body != null && !headers['Content-Type'] && !headers['content-type']) {
        // text/plain is CORS-safelisted (no preflight). AppSail edge OPTIONS
        // omits ACAO, so application/json POSTs fail in the browser.
        headers['Content-Type'] = 'text/plain;charset=UTF-8';
    }
    const config = {
        ...options,
        method,
        headers,
    };

    const response = await fetch(url, config);
    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }
    return response.json();
}

export function get(path) {
    return apiRequest(path);
}

export function post(path, data) {
    return apiRequest(path, { method: 'POST', body: JSON.stringify(data) });
}

export function put(path, data) {
    return apiRequest(path, { method: 'PUT', body: JSON.stringify(data) });
}

export function del(path) {
    return apiRequest(path);
}

export function stream(path, data, onChunk, onDone) {
    const controller = new AbortController();
    fetch(`${API_BASE}${path}`, {
        method: 'POST',
        headers: { 'Content-Type': 'text/plain;charset=UTF-8' },
        body: JSON.stringify(data),
        signal: controller.signal,
    }).then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        function read() {
            reader.read().then(({ done, value }) => {
                if (done) { onDone(); return; }
                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop();
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const chunk = JSON.parse(line.slice(6));
                            if (chunk.done) { onDone(); return; }
                            if (chunk.content) { onChunk(chunk.content); }
                        } catch { /* ignore malformed chunk */ }
                    }
                }
                read();
            });
        }
        read();
    }).catch(err => {
        console.error('Stream error:', err);
        onDone();
    });
    return controller;
}
