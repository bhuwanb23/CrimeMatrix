export const districts = [
  { id: 'BLR', name: 'Bengaluru Urban', cases: 451, x: 420, y: 320, hotspots: 5, risk: 'high' },
  { id: 'BLR-R', name: 'Bengaluru Rural', cases: 89, x: 400, y: 350, hotspots: 1, risk: 'medium' },
  { id: 'MYS', name: 'Mysuru', cases: 186, x: 300, y: 400, hotspots: 3, risk: 'high' },
  { id: 'MNG', name: 'Mangaluru', cases: 95, x: 220, y: 380, hotspots: 2, risk: 'medium' },
  { id: 'HBL', name: 'Hubballi-Dharwad', cases: 42, x: 280, y: 180, hotspots: 1, risk: 'low' },
  { id: 'GNT', name: 'Gulbarga', cases: 38, x: 420, y: 120, hotspots: 1, risk: 'low' },
  { id: 'BJR', name: 'Belgaum', cases: 55, x: 200, y: 150, hotspots: 1, risk: 'medium' },
  { id: 'OGD', name: 'Ongole', cases: 32, x: 480, y: 250, hotspots: 0, risk: 'low' },
]

export const hotspots = [
  { id: 'H1', name: 'Malleshwaram', district: 'BLR', cases: 28, x: 410, y: 310, severity: 'high' },
  { id: 'H2', name: 'Whitefield', district: 'BLR', cases: 22, x: 445, y: 325, severity: 'high' },
  { id: 'H3', name: 'Electronic City', district: 'BLR', cases: 18, x: 415, y: 345, severity: 'medium' },
  { id: 'H4', name: 'Koramangala', district: 'BLR', cases: 15, x: 425, y: 335, severity: 'medium' },
  { id: 'H5', name: 'Indiranagar', district: 'BLR', cases: 12, x: 435, y: 315, severity: 'medium' },
  { id: 'H6', name: 'Mysuru City', district: 'MYS', cases: 20, x: 305, y: 395, severity: 'high' },
  { id: 'H7', name: 'Hunsur', district: 'MYS', cases: 8, x: 285, y: 410, severity: 'low' },
  { id: 'H8', name: 'Mangaluru City', district: 'MNG', cases: 15, x: 225, y: 375, severity: 'medium' },
  { id: 'H9', name: 'Puttur', district: 'MNG', cases: 6, x: 210, y: 395, severity: 'low' },
  { id: 'H10', name: 'Hubballi City', district: 'HBL', cases: 10, x: 285, y: 175, severity: 'medium' },
  { id: 'H11', name: 'Dharwad', district: 'HBL', cases: 7, x: 270, y: 185, severity: 'low' },
  { id: 'H12', name: 'Gulbarga City', district: 'GNT', cases: 8, x: 425, y: 115, severity: 'low' },
]

export const routes = [
  { from: 'BLR', to: 'MYS', type: 'suspect-movement', label: 'Suspect transit' },
  { from: 'BLR', to: 'MNG', type: 'evidence-link', label: 'Evidence connection' },
  { from: 'MYS', to: 'MNG', type: 'case-link', label: 'Related cases' },
  { from: 'BLR', to: 'HBL', type: 'phone-link', label: 'Phone records' },
]

export const crimeDensity = [
  { level: 'high', color: '#ef4444', label: 'High (>100 cases)', count: 2 },
  { level: 'medium', color: '#f59e0b', label: 'Medium (50-100)', count: 3 },
  { level: 'low', color: '#10b981', label: 'Low (<50)', count: 3 },
]

export const karnatakaOutline = 'M 150 80 L 200 60 L 280 70 L 350 90 L 420 100 L 480 140 L 520 200 L 530 280 L 510 340 L 480 400 L 420 450 L 350 470 L 280 460 L 220 430 L 180 380 L 160 320 L 140 260 L 130 200 L 140 140 Z'
