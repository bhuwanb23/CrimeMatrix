import { get, post } from './api';

export async function getSimilarCases(caseId, topK = 10) {
    return get(`/similar-cases/${caseId}?top_k=${topK}`);
}

export async function compareCases(caseId1, caseId2) {
    return get(`/similar-cases/compare/${caseId1}/${caseId2}`);
}

export async function computeSimilarities(caseId = null, force = false) {
    return post('/similar-cases/compute', { case_id: caseId, force });
}

export async function getSimilarityStats() {
    return get('/similar-cases/stats');
}
