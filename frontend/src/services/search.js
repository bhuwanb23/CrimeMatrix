import { get, post, del } from './api';

export async function searchCrimes(query, filters = {}, page = 1, perPage = 20) {
    return post('/search/', { query, filters, page, page_size: perPage });
}

export async function searchKeyword(query) {
    return post('/search/keyword', { query });
}

export async function getFacets(entity = 'cases') {
    return get(`/search/facets?entity=${entity}`);
}

export async function getSuggestions(query) {
    return get(`/search/suggestions?q=${encodeURIComponent(query)}`);
}

export async function listSavedSearches(userId = 'default') {
    return get(`/search/saved?user_id=${userId}`);
}

export async function saveSearch(name, query, filters = null) {
    return post('/search/saved', { name, query, filters, user_id: 'default' });
}

export async function deleteSavedSearch(id) {
    return del(`/search/saved/${id}`);
}

export async function listSearchHistory(userId = 'default') {
    return get(`/search/history?user_id=${userId}`);
}

export async function recordSearch(query, resultsCount = 0) {
    return post('/search/history', { query, results_count: resultsCount, user_id: 'default' });
}

export async function clearSearchHistory() {
    return del('/search/history');
}

export async function semanticSearch(query, topK = 5, docType = null) {
    return post('/search/semantic', { query, top_k: topK, doc_type: docType });
}

export async function indexDocuments() {
    return post('/search/semantic/index');
}

export async function getSemanticStats() {
    return get('/search/semantic/stats');
}
