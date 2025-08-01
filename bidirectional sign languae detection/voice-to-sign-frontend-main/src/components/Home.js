import React from "react";
import { useNavigate } from "react-router-dom";
import { FaMicrophoneAlt, FaRegFileAlt } from "react-icons/fa";
import './Home.css';
import Navbar from './Navbar';

const Home = () => {
  const navigate = useNavigate();

  return (
    <>
      <Navbar />
      <div className="home-container">
        <font color="blue"><h1 className="home-title">Bidirectional Sign Language Translator</h1></font>

        <div className="home-grid">
          {/* Voice to Sign card */}
          <div
            onClick={() => navigate("/voice-to-sign")}
            className="home-card"
            role="button"
            tabIndex={0}
            onKeyPress={() => navigate("/voice-to-sign")}
          >
            <div className="icon-wrapper">
              <FaMicrophoneAlt size={36} />
            </div>
            <h2 className="home-card-title">Voice to Sign</h2>
            <p className="home-card-desc">Convert voice into sign language using AI models.</p>
          </div>

          {/* Sign to Text card — updated to use external link */}
          <div
            onClick={() => window.location.href = "http://127.0.0.1:5000/index"}
            className="home-card"
            role="button"
            tabIndex={0}
            onKeyPress={() => window.location.href = "http://127.0.0.1:5000/index"}
          >
            <div className="icon-wrapper">
              <FaRegFileAlt size={36} />
            </div>
            <h2 className="home-card-title">Sign to Text</h2>
            <p className="home-card-desc">Convert written text into sign language gifs.</p>
          </div>
        </div>
      </div>
    </>
  );
};

export default Home;
