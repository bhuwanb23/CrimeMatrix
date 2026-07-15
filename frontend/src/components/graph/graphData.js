export const nodes = [
  // Suspects
  { id: 'RK', type: 'suspect', label: 'Ravi Kumar', risk: 92, cases: 5, x: 200, y: 150, gradient: 'linear-gradient(135deg, #ef4444, #dc2626)' },
  { id: 'DR', type: 'suspect', label: 'Deepak Reddy', risk: 88, cases: 7, x: 400, y: 200, gradient: 'linear-gradient(135deg, #6366f1, #4f46e5)' },
  { id: 'MA', type: 'suspect', label: 'Mohammed Ali', risk: 78, cases: 3, x: 350, y: 80, gradient: 'linear-gradient(135deg, #f59e0b, #d97706)' },
  { id: 'IK', type: 'suspect', label: 'Imran Khan', risk: 70, cases: 3, x: 550, y: 250, gradient: 'linear-gradient(135deg, #f97316, #ea580c)' },
  { id: 'VR', type: 'suspect', label: 'Venkatesh Reddy', risk: 65, cases: 4, x: 150, y: 320, gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)' },
  { id: 'RS', type: 'suspect', label: 'Rajesh Sharma', risk: 82, cases: 6, x: 500, y: 100, gradient: 'linear-gradient(135deg, #3b82f6, #2563eb)' },

  // Evidence
  { id: 'E1', type: 'evidence', label: 'CCTV #4521', x: 100, y: 200, icon: '📹' },
  { id: 'E2', type: 'evidence', label: 'Phone Records', x: 300, y: 350, icon: '📱' },
  { id: 'E3', type: 'evidence', label: 'Fingerprint', x: 250, y: 100, icon: '🔍' },

  // Vehicles
  { id: 'V1', type: 'vehicle', label: 'KA-01-AB-1234', x: 600, y: 180, icon: '🏍️' },
  { id: 'V2', type: 'vehicle', label: 'KA-05-CD-5678', x: 450, y: 350, icon: '🚗' },

  // Phones
  { id: 'P1', type: 'phone', label: '+91 98765 43210', x: 120, y: 100, icon: '📞' },
  { id: 'P2', type: 'phone', label: '+91 87654 32109', x: 480, y: 50, icon: '📞' },
]

export const edges = [
  // Accomplice relationships
  { source: 'RK', target: 'DR', type: 'accomplice', label: 'Operational Head' },
  { source: 'RK', target: 'MA', type: 'accomplice', label: 'Training' },
  { source: 'DR', target: 'IK', type: 'accomplice', label: 'Logistics' },
  { source: 'DR', target: 'RS', type: 'accomplice', label: 'Cyber Ops' },
  { source: 'IK', target: 'VR', type: 'fence', label: 'Parts Dealer' },

  // Evidence links
  { source: 'RK', target: 'E1', type: 'evidence', label: 'Identified' },
  { source: 'RK', target: 'E2', type: 'evidence', label: 'Cell tower' },
  { source: 'DR', target: 'E3', type: 'evidence', label: 'Partial print' },

  // Vehicle links
  { source: 'IK', target: 'V1', type: 'vehicle', label: 'Registered' },
  { source: 'DR', target: 'V2', type: 'vehicle', label: 'Used in crime' },

  // Phone links
  { source: 'RK', target: 'P1', type: 'phone', label: 'Primary' },
  { source: 'DR', target: 'P2', type: 'phone', label: ' burner' },
  { source: 'RS', target: 'P2', type: 'phone', label: 'Shared' },
]

export const edgeColors = {
  accomplice: '#ef4444',
  fence: '#f59e0b',
  evidence: '#3b82f6',
  vehicle: '#8b5cf6',
  phone: '#10b981',
}

export const nodeColors = {
  suspect: '#0f172a',
  evidence: '#3b82f6',
  vehicle: '#8b5cf6',
  phone: '#10b981',
}
