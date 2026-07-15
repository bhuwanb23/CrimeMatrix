import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardContent from './components/DashboardContent'
import CopilotPage from './components/CopilotPage'
import SearchPage from './components/SearchPage'
import CaseDetailPage from './components/CaseDetailPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardContent />} />
          <Route path="/copilot" element={<CopilotPage />} />
          <Route path="/cases" element={<SearchPage />} />
          <Route path="/cases/:id" element={<CaseDetailPage />} />
          <Route path="/analytics" element={<DashboardContent />} />
          <Route path="/stations" element={<DashboardContent />} />
          <Route path="/suspects" element={<DashboardContent />} />
          <Route path="/investigations" element={<DashboardContent />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
