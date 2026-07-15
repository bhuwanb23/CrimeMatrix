import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardContent from './components/DashboardContent'
import CopilotPage from './components/CopilotPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardContent />} />
          <Route path="/copilot" element={<CopilotPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
