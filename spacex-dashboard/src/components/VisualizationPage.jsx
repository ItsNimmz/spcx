import { useEffect, useState } from 'react'
import axios from 'axios'
import { 
  BarChart, Bar, LineChart, Line, 
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, 
  ResponsiveContainer, ComposedChart 
} from 'recharts'

export default function VisualizationPage({ onBack }) {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/launches/stats')
        setStats(response.data)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  return (
    <div className="page-container">
      <button className="back-btn" onClick={onBack}>
        ← Back
      </button>
      
      <h2>Launch Visualizations</h2>
      
      {loading ? (
        <div className="loading">Loading data...</div>
      ) : (
        <div className="visualization-grid">
          <div className="grid">
            <div className="chart-card">
            <h2>Launch Success Rate Over Time</h2>
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={stats.yearly_stats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis domain={[0, 100]} />
                <Tooltip 
                    formatter={(value) => [`${value}%`, "Success Rate"]}
                    labelFormatter={(year) => `Year: ${year}`}
                />
                <Legend />
                <Line 
                    type="monotone" 
                    dataKey="success_rate" 
                    stroke="#4CAF50" 
                    strokeWidth={2}
                    activeDot={{ r: 6 }}
                    name="Success Rate (%)"
                />
                </LineChart>
            </ResponsiveContainer>
            </div>
            {/* New Launch Count Chart */}
            <div className="chart-card">
            <h2>Launches Per Year</h2>
            <ResponsiveContainer width="100%" height={400}>
                <BarChart data={stats.yearly_stats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis />
                <Tooltip 
                    formatter={(value) => [value, "Launches"]}
                    labelFormatter={(year) => `Year: ${year}`}
                />
                <Legend />
                <Bar 
                    dataKey="total_launches" 
                    fill="#8884d8" 
                    name="Total Launches"
                    radius={[4, 4, 0, 0]}
                />
                </BarChart>
            </ResponsiveContainer>
            </div>

            <div className="chart-card">
            <h2>Payload Capacity by Rocket</h2>
            <ResponsiveContainer width="100%" height={400}>
                <BarChart data={stats.rocket_stats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="rocket" />
                <YAxis />
                <Tooltip 
                    formatter={(value) => [`${value} kg`, "Payload Mass"]}
                    labelFormatter={(rocket) => `Rocket: ${rocket}`}
                />
                <Legend />
                <Bar 
                    dataKey="avg_payload" 
                    fill="#FF9800" 
                    name="Avg Payload (kg)"
                    radius={[4, 4, 0, 0]}
                />
                <Bar 
                    dataKey="total_payload" 
                    fill="#2196F3" 
                    name="Total Payload (kg)"
                    radius={[4, 4, 0, 0]}
                />
                </BarChart>
            </ResponsiveContainer>
            </div>
        </div>
        </div>
      )}
    </div>
  )
}