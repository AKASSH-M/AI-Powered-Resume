import React from 'react';
import './global.css';

function About() {
  return (
    <section id="about" className="about-section">
      <div className="container">
        <h2>About Us</h2>
        <p>
          Welcome to <strong>AI-Powered Resume</strong> — your smart assistant for building a better future. Our platform uses advanced AI technology to analyze and improve your resume, ensuring it stands out in today's competitive job market.
        </p>
        <p>
          Whether you're a student, a recent graduate, or a working professional, our goal is to help you create resumes that are clear, keyword-rich, and tailored for your target roles. We provide real-time feedback on structure, content, and relevance.
        </p>
        <p>
          This project is built using React and showcases how modern web technologies and artificial intelligence can come together to create impactful tools for career growth.
        </p>
      </div>
    </section>
  );
}

export default About;