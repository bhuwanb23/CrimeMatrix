import { useState, useCallback } from 'react'
import Layout from './components/Layout'
import DashboardContent from './components/DashboardContent'
import CopilotPage from './components/CopilotPage'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')

  const handleNavigate = useCallback((page) => {
    setCurrentPage(page)
  }, [])

  return (
    <Layout onNavigate={handleNavigate} currentPage={currentPage}>
      {currentPage === 'copilot' ? <CopilotPage /> : <DashboardContent />}
    </Layout>
  )
}

export default App
