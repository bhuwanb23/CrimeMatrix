import { get, post, del } from './api'

export async function listReportTemplates() {
  return get('/reports/templates')
}

export async function getReportTemplate(templateId) {
  return get(`/reports/templates/${templateId}`)
}

export async function listReportQueue() {
  return get('/reports/queue')
}

export async function queueReport(reportType, crimeId, templateId = null) {
  return post('/reports/queue', {
    report_type: reportType,
    crime_id: crimeId,
    template_id: templateId,
  })
}

export async function cancelReportJob(jobId) {
  return del(`/reports/queue/${jobId}`)
}

export async function generateSummaryReport(crimeId, templateId = null) {
  return post('/reports/generate/summary', { crime_id: crimeId, template_id: templateId })
}

export async function generateTimelineReport(crimeId, templateId = null) {
  return post('/reports/generate/timeline', { crime_id: crimeId, template_id: templateId })
}

export async function generateEvidenceReport(crimeId, templateId = null) {
  return post('/reports/generate/evidence', { crime_id: crimeId, template_id: templateId })
}

export async function generateInvestigationReport(crimeId, templateId = null) {
  return post('/reports/generate/investigation', { crime_id: crimeId, template_id: templateId })
}
