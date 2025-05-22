import React from 'react';
import './home.css';

function Home() {
  return (
    <section id="home">
      <div className="home-container">
        <h2>Upload your resume to analyze it with AI</h2>
        <p>Our system will scan and extract valuable insights from your resume.</p>

        <form>
          <div className="file-upload-wrapper">
            <input type="file" id="resumeUpload" accept=".pdf" />
            <label htmlFor="resumeUpload" className="upload-label">
              📄 Choose Resume (PDF)
            </label>
          </div>
          <button type="submit" className="analyze-btn">Analyze Resume</button>
        <p className="format-note">Please upload your resume in PDF format</p>

        </form>
      </div>
    </section>
  );
}

export default Home;
