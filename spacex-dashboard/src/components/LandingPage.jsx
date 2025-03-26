export default function LandingPage({ onNavigate }) {
    return (
      <div className="landing-container">
        <div className="landing-content">
          <h1>SpaceX Launch Analytics</h1>
          <p className="description">
            Explore SpaceX's launch history with interactive visualizations 
            and detailed performance metrics. Discover trends in launch success rates,
            payload capacities, and mission statistics.
          </p>
          
          <div className="button-group">
            <button 
              className="primary-btn"
              onClick={() => onNavigate('visualization')}
            >
              Show Visualizations
            </button>
            <button 
              className="secondary-btn"
              onClick={() => onNavigate('metrics')}
            >
              Show Metrics
            </button>
          </div>
        </div>
      </div>
    )
  }