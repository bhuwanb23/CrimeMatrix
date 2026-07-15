export const crimeTypes = [
  { name: 'Theft', count: 451, percentage: 35.1, color: '#f59e0b' },
  { name: 'Fraud', count: 353, percentage: 27.5, color: '#3b82f6' },
  { name: 'Cybercrime', count: 261, percentage: 20.3, color: '#8b5cf6' },
  { name: 'Assault', count: 142, percentage: 11.1, color: '#ef4444' },
  { name: 'Other', count: 77, percentage: 6.0, color: '#94a3b8' },
]

export const monthlyTrend = [
  { month: 'Jan', cases: 95, resolved: 72 },
  { month: 'Feb', cases: 88, resolved: 65 },
  { month: 'Mar', cases: 102, resolved: 78 },
  { month: 'Apr', cases: 115, resolved: 89 },
  { month: 'May', cases: 98, resolved: 75 },
  { month: 'Jun', cases: 110, resolved: 82 },
  { month: 'Jul', cases: 125, resolved: 91 },
  { month: 'Aug', cases: 118, resolved: 85 },
  { month: 'Sep', cases: 105, resolved: 80 },
  { month: 'Oct', cases: 95, resolved: 72 },
  { month: 'Nov', cases: 88, resolved: 68 },
  { month: 'Dec', cases: 92, resolved: 70 },
]

export const districtRanking = [
  { district: 'Bengaluru Urban', cases: 555, percentage: 43.2, color: '#f59e0b' },
  { district: 'Mysuru', cases: 353, percentage: 27.5, color: '#3b82f6' },
  { district: 'Mangaluru', cases: 186, percentage: 14.5, color: '#8b5cf6' },
  { district: 'Hubballi', cases: 115, percentage: 9.0, color: '#10b981' },
  { district: 'Other', cases: 75, percentage: 5.8, color: '#94a3b8' },
]

export const resolutionCohorts = [
  { period: '0-30 days', resolved: 420, total: 580, percentage: 72 },
  { period: '31-60 days', resolved: 310, total: 420, percentage: 74 },
  { period: '61-90 days', resolved: 180, total: 280, percentage: 64 },
  { period: '91-180 days', resolved: 95, total: 190, percentage: 50 },
  { period: '180+ days', resolved: 35, total: 120, percentage: 29 },
]

export const todayStats = {
  total: 571,
  theft: 293,
  fraud: 161,
  cyber: 117,
}

export const crimeSummary = {
  totalCases: 1284,
  totalResolved: 948,
  resolutionRate: 73.8,
  avgResolutionDays: 42,
}
