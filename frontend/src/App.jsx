import Layout from './components/Layout'

function App() {
  return (
    <Layout>
      <div className="p-8">
        <h1 className="text-2xl font-semibold text-[var(--text-heading)] mb-2">
          Crime Intelligence Copilot
        </h1>
        <p className="text-[var(--text-muted)]">
          Welcome to KSP CrimeMatrix — AI-powered investigation assistant for Karnataka State Police.
        </p>
      </div>
    </Layout>
  )
}

export default App
