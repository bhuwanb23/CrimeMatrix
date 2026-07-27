import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { LanguageProvider } from './context/LanguageContext'
import { ThemeProvider } from './context/ThemeContext'
import { OnboardingProvider } from './context/OnboardingContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ThemeProvider>
      <LanguageProvider>
        <OnboardingProvider>
          <App />
        </OnboardingProvider>
      </LanguageProvider>
    </ThemeProvider>
  </StrictMode>,
)

