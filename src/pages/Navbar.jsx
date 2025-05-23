import React from 'react';
import Logo from '../Logo.png';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar-container">
      <div className="navbar-content">
        <div className="navbar-logo-container">
          <img 
            src={Logo} 
            alt="App Logo" 
            className="navbar-logo"
          />
          <span className="app-name">Serenity</span>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;