import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import DashboardContent from './components/DashboardContent'
import CopilotPage from './components/CopilotPage'
import SearchPage from './components/SearchPage'
import CaseDetailPage from './components/CaseDetailPage'
import InvestigationPage from './components/InvestigationPage'
import SuspectsPage from './components/SuspectsPage'
import SuspectDetailPage from './components/SuspectDetailPage'
import GraphPage from './components/GraphPage'
import AnalyticsPage from './components/AnalyticsPage'
import MapPage from './components/MapPage'
import AlertsPage from './components/AlertsPage'
import ReportsPage from './components/ReportsPage'
import SettingsPage from './components/SettingsPage'
import BookmarksPage from './components/BookmarksPage'
import CrimeIntelligencePage from './components/CrimeIntelligencePage'
import PatternDiscoveryPage from './components/PatternDiscoveryPage'
import CriminalTimelinePage from './components/CriminalTimelinePage'
import AIAnalyticsPage from './components/AIAnalyticsPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<DashboardContent />} />
          <Route path="/copilot" element={<CopilotPage />} />
          <Route path="/cases" element={<SearchPage />} />
          <Route path="/cases/:id" element={<CaseDetailPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/intelligence" element={<CrimeIntelligencePage />} />
          <Route path="/patterns" element={<PatternDiscoveryPage />} />
          <Route path="/timeline" element={<CriminalTimelinePage />} />
          <Route path="/analytics-dashboard" element={<AIAnalyticsPage />} />
          <Route path="/knowledge-graph" element={<GraphPage />} />
          <Route path="/stations" element={<MapPage />} />
          <Route path="/suspects" element={<SuspectsPage />} />
          <Route path="/suspects/:id" element={<SuspectDetailPage />} />
          <Route path="/investigations" element={<InvestigationPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/bookmarks" element={<BookmarksPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
