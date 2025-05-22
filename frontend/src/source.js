// Source.js
import React from 'react';
import './global.css';


function Source() {
  return (
    <section id="Source" className="source-section">
      <div className="container">
        <h2>Project Source</h2>
        <p>
          You can explore the complete source code of this AI-powered resume analyzer on GitHub. 
          Feel free to fork the repo, contribute, or use it as inspiration for your own projects.
        </p>
        <a 
          href="https://github.com/AKASSH-M/AI-Powered-Resume.git" 
          target="_blank" 
          rel="noopener noreferrer"
          className="source-link"
        >
          🔗 View on GitHub
        </a>
      </div>
    </section>
  );
}

export default Source;
