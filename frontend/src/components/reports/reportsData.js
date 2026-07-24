export const getReports = (t) => [
  { id: 'RPT-001', title: `${t('Investigation Report')} — ${t('FIR')} #4521`, type: 'investigation', status: 'active', date: t('Jul 15, 2026'), caseId: `${t('FIR')} #4521`, officer: t('SI Karthik'), pages: 12, size: '2.4 MB' },
  { id: 'RPT-002', title: `${t('Court Report')} — ${t('Theft Case')} #4489`, type: 'court', status: 'filed', date: t('Jul 14, 2026'), caseId: `${t('FIR')} #4489`, officer: t('Inspector Deepak'), pages: 18, size: '3.1 MB' },
  { id: 'RPT-003', title: `${t('Investigation Report')} — ${t('FIR')} #4515`, type: 'investigation', status: 'draft', date: t('Jul 13, 2026'), caseId: `${t('FIR')} #4515`, officer: t('SI Priya'), pages: 8, size: '1.8 MB' },
  { id: 'RPT-004', title: `${t('Court Report')} — ${t('Fraud Case')} #4498`, type: 'court', status: 'pending', date: t('Jul 12, 2026'), caseId: `${t('FIR')} #4498`, officer: t('Inspector Deepak'), pages: 15, size: '2.9 MB' },
  { id: 'RPT-005', title: `${t('Investigation Report')} — ${t('FIR')} #4508`, type: 'investigation', status: 'final', date: t('Jul 11, 2026'), caseId: `${t('FIR')} #4508`, officer: t('SI Karthik'), pages: 22, size: '4.2 MB' },
  { id: 'RPT-006', title: `${t('Export')} — ${t('Monthly Summary July')}`, type: 'export', status: 'final', date: t('Jul 10, 2026'), caseId: t('Monthly'), officer: t('System'), pages: 35, size: '5.8 MB' },
  { id: 'RPT-007', title: `${t('Court Report')} — ${t('Assault Case')} #4495`, type: 'court', status: 'filed', date: t('Jul 9, 2026'), caseId: `${t('FIR')} #4495`, officer: t('SI Priya'), pages: 10, size: '1.5 MB' },
  { id: 'RPT-008', title: `${t('Investigation Report')} — ${t('FIR')} #4501`, type: 'investigation', status: 'active', date: t('Jul 8, 2026'), caseId: `${t('FIR')} #4501`, officer: t('Inspector Deepak'), pages: 14, size: '2.7 MB' },
  { id: 'RPT-009', title: `${t('Export')} — ${t('Suspect Network Report')}`, type: 'export', status: 'final', date: t('Jul 7, 2026'), caseId: t('Network'), officer: t('System'), pages: 28, size: '4.5 MB' },
  { id: 'RPT-010', title: `${t('Investigation Report')} — ${t('FIR')} #4485`, type: 'investigation', status: 'draft', date: t('Jul 6, 2026'), caseId: `${t('FIR')} #4485`, officer: t('SI Karthik'), pages: 6, size: '1.2 MB' },
  { id: 'RPT-011', title: `${t('Court Report')} — ${t('Cybercrime')} #4485`, type: 'court', status: 'pending', date: t('Jul 5, 2026'), caseId: `${t('FIR')} #4485`, officer: t('Inspector Deepak'), pages: 20, size: '3.5 MB' },
  { id: 'RPT-012', title: `${t('Investigation Report')} — ${t('FIR')} #4475`, type: 'investigation', status: 'final', date: t('Jul 4, 2026'), caseId: `${t('FIR')} #4475`, officer: t('SI Priya'), pages: 16, size: '2.8 MB' },
]

export const reportTypes = {
  investigation: { color: '#3b82f6', label: 'Investigation' },
  court: { color: '#f59e0b', label: 'Court Report' },
  export: { color: '#10b981', label: 'Export' },
}

export const reportStatuses = {
  draft: { color: '#94a3b8', label: 'Draft' },
  active: { color: '#3b82f6', label: 'Active' },
  pending: { color: '#f59e0b', label: 'Pending' },
  filed: { color: '#10b981', label: 'Filed' },
  final: { color: '#8b5cf6', label: 'Final' },
}

export const weeklyData = [
  { day: 'Mon', investigation: 5, court: 3, export: 1 },
  { day: 'Tue', investigation: 4, court: 2, export: 2 },
  { day: 'Wed', investigation: 6, court: 4, export: 1 },
  { day: 'Thu', investigation: 3, court: 2, export: 3 },
  { day: 'Fri', investigation: 7, court: 5, export: 2 },
  { day: 'Sat', investigation: 2, court: 1, export: 1 },
  { day: 'Sun', investigation: 1, court: 0, export: 0 },
]
