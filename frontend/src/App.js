import React from 'react';
import './App.css';
import logo from './logo.svg';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import Home from './home';
import About from './about';
import Source from './source';
import Contact from './contact';

function App() {
  return (
    <Router>
      <div className="App">
        <header>
          <nav id="navbar">
            <img src={logo} className="App-logo" alt="logo" />
            <h1>AI-Powered Resume</h1>
            <ul>
              <li><Link to="/">Home</Link></li>
              <li><Link to="/about">About</Link></li>
              <li><Link to="/source">Source</Link></li>
              <li><Link to="/contact">Contact</Link></li>
            </ul>
          </nav>
        </header>

        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/source" element={<Source />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>

        <footer>
          <p>&copy; 2025 AI-Powered Resume. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
