import { useState } from 'react'
import LandingPage from './components/LandingPage'
import VisualizationPage from './components/VisualizationPage'
import MetricsPage from './components/MetricsPage'
import './App.css'

function App() {
  const [view, setView] = useState('landing') // 'landing', 'visualization', 'metrics'

  return (
    <div className="app-container">
      {view === 'landing' && (
        <LandingPage onNavigate={setView} />
      )}
      {view === 'visualization' && (
        <VisualizationPage onBack={() => setView('landing')} />
      )}
      {view === 'metrics' && (
        <MetricsPage onBack={() => setView('landing')} />
      )}
    </div>
  )
}

export default App