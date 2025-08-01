import React from 'react';

const Footer = () => {
  return (
    <footer
      style={{
        backgroundColor: '#f0f0f0',
        padding: '20px',
        marginTop: '40px',
        textAlign: 'center',
        fontSize: '0.9rem',
        borderTop: '1px solid #ccc',
      }}
    >
      <div style={{ marginBottom: '10px' }}>
        <strong>About this App:</strong> <br />
        This web app converts your voice or typed input into sign language using text and gifs.
        It is built to help bridge the communication gap with the hearing impaired.
      </div>
      <div>Made with ❤️ for accessibility. © 2025</div>
    </footer>
  );
};

export default Footer;
