// Contact.js
import React from 'react';
import './global.css';

function Contact() {
  return (
    <section id="contact" className="section">
      <div className="container">
        <h2>Contact</h2>
        <p>
          This project was developed collaboratively as part of a team effort. For any questions or feedback, please feel free to connect with the contributors individually.
        </p>
        <p>
          Contributor contact details are available in the{' '}
          <a
            href="https://github.com/AKASSH-M/AI-Powered-Resume.git" 
            target="_blank"
            rel="noopener noreferrer"
            className="readme-link"
          >
            GitHub repository README
          </a>.
        </p>
      </div>
    </section>
  );
}

export default Contact;
