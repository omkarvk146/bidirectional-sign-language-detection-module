import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import VoiceToSign from './components/VoiceToSign';
import SignToText from './components/SignToText';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <div className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/voice-to-sign" element={<VoiceToSign />} />
            <Route path="/sign-to-text" element={<SignToText />} />
          </Routes>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App;
