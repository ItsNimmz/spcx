import React from 'react';

// Card component to display a section
const Card = ({ title, children }) => {
  return (
    <div className="card" style={styles.card}>
      <h3 style={styles.cardHeading}>{title}</h3>
      <div style={styles.cardContent}>{children}</div>
    </div>
  );
};

const styles = {
  card: {
    backgroundColor: '#2d3748',
    borderRadius: '10px',
    boxShadow: '0 4px 10px rgba(0, 0, 0, 0.1)',
    padding: '20px',
    marginBottom: '20px',
    color: '#f4f7fc',
  },
  cardHeading: {
    fontSize: '1.4rem',
    marginBottom: '10px',
  },
  cardContent: {
    fontSize: '1rem',
    color: '#bbb',
  },
};

export default Card;
