import React, { useState, useEffect } from 'react';
import axios from 'axios';  // Import axios for HTTP requests
import Card from './Card';  // Import the Card component

export default function MetricsPage({ onBack }) {
  const [launchData, setLaunchData] = useState(null);  // State to store fetched data
  const [loading, setLoading] = useState(true);  // State to handle loading status
  const [error, setError] = useState(null);  // State to handle errors

  useEffect(() => {
    // Fetch data from Flask API on component mount
    axios
      .get('http://localhost:5000/api/launches/metrix')  // URL of the Flask API
      .then((response) => {
        setLaunchData(response.data);  // Set data to state
        setLoading(false);  // Set loading to false after data is fetched
      })
      .catch((err) => {
        console.error('Error fetching data:', err);
        setError('Failed to load data');
        setLoading(false);  // Set loading to false in case of error
      });
  }, []);

  // If loading, show a loading message
  if (loading) {
    return <div>Loading...</div>;
  }

  // If there is an error, show the error message
  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="page-container" style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <button className="back-btn" onClick={onBack}>
        ← Back
      </button>
      <h2>Launch Metrics</h2>

      <div className="metrics-container" style={styles.metricsContainer}>
        {/* Total Launches Card */}
        <Card title="Total Launches">
          <p>{launchData.totalLaunches}</p>
        </Card>

        {/* Success Rate Card */}
        <Card title="Success Rate">
          <p>{launchData.successRate}%</p>
        </Card>

        {/* Reused Rockets Percentage Card */}
        <Card title="Percentage of Reused Rockets">
          <p>{launchData.reusedRocketsPercentage}%</p>
        </Card>

        {/* Distribution of Payload Types Card */}
        <Card title="Distribution of Payload Types">
          <ul>
            {Object.entries(launchData.payloadTypeDistribution).map(([payload, count]) => (
              <li key={payload}>
                {payload}: {count}
              </li>
            ))}
          </ul>
        </Card>

        {/* Launches by Rocket Type Card */}
        <Card title="Launches by Rocket Type">
          <ul>
            {Object.entries(launchData.launchesByRocketType).map(([rocketType, count]) => (
              <li key={rocketType}>
                {rocketType}: {count}
              </li>
            ))}
          </ul>
        </Card>

        {/* Average Payload Mass Card */}
        <Card title="Average Payload Mass">
          <p>Successful Launches: {launchData.avgPayloadMass.successfulLaunches} kg</p>
          <p>Failed Launches: {launchData.avgPayloadMass.failedLaunches} kg</p>
        </Card>

        {/* Launch Frequencies per Year Card */}
        <Card title="Launch Frequencies per Year">
          <ul>
            {Object.entries(launchData.launchFrequencyByYear).map(([year, count]) => (
              <li key={year}>
                {year}: {count} 
              </li>
            ))}
          </ul>
        </Card>

          {/* Success Rate by Nationality Card */}
          <Card title="Success Rate by Nationality">
          <ul>
            {Object.entries(launchData.successRateByNationality).map(([nationality, rate]) => (
              <li key={nationality}>
                {nationality}: {rate}%
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  );
}

const styles = {
    backBtn: {
      backgroundColor: '#2d3748',
      color: '#f4f7fc',
      padding: '10px 20px',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      fontSize: '16px',
      marginBottom: '20px', // Optional: Add margin below the button
    },
    metricsContainer: {
      display: 'grid',
      gridTemplateColumns: 'repeat(3, 1fr)', // Ensure three columns
      gap: '20px',
    },
  };
