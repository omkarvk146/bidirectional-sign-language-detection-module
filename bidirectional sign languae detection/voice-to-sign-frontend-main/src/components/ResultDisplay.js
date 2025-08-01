import React from 'react';

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  if (result.type === 'gif') {
    return (
      <div style={{ marginTop: 20 }}>
        <h3>Sign Language GIF</h3>
        <img
          src={`/gifs/${result.value}.gif`}
          alt={result.value}
          style={{ height: 200 }}
        />
      </div>
    );
  }

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Here’s your hand signs</h3>
      <div style={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap' }}>
        {result.value.map((char, index) => (
          <img
            key={index}
            src={`/letters/${char}.jpg`}
            alt={char}
            style={{ height: 100, margin: 5 }}
          />
        ))}
      </div>
    </div>
  );
};

export default ResultDisplay;
