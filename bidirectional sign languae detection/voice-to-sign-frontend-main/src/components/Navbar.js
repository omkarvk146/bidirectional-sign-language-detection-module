import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';  // We'll create this CSS next

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo"></div>
        <div className="navbar-links">
          <NavLink
            to="/"
            className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
          >
            Home
          </NavLink>
          <NavLink
            to="/voice-to-sign"
            className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
          >
            Voice to Sign
          </NavLink>
          <NavLink
            to="/sign-to-text"
            className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}
          >
            Sign to Text
          </NavLink>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
