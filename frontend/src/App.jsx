import { useState, useCallback } from 'react'
import Layout from './components/Layout'
import DashboardContent from './components/DashboardContent'
import CopilotPage from './components/CopilotPage'

function App() {
  const [currentPage, setCurrentPage] = useState('dashboard')

  const handleNavigate = useCallback((page) => {
    setCurrentPage(page)
  }, [])

  const handleBackToDashboard = useCallback(() => {
    setCurrentPage('dashboard')
  }, [])

  if (currentPage === 'copilot') {
    return <CopilotPage onBack={handleBackToDashboard} />
  }

  return (
    <Layout onNavigate={handleNavigate} currentPage={currentPage}>
      <DashboardContent />
    </Layout>
  )
}

export default App
