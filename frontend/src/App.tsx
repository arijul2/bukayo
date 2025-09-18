import React from "react";
import FileUpload from "./components/FileUpload";
import JobDescriptionUpload from "./components/JobDescriptionUpload";
import "./ModernStyles.css";

function App() {
  return (
    <div className="modern-app">
      {/* Modern Header with Gradient */}
      <header className="modern-header">
        <div className="header-content">
          <div className="logo-section">
            <div className="logo-icon">🚀</div>
            <h1 className="app-title">JobMatch AI</h1>
          </div>
          <p className="app-subtitle">Smart Resume Analysis & Job Matching</p>
        </div>
        <div className="header-gradient"></div>
      </header>

      {/* Main Content */}
      <main className="main-content">
        <div className="container">
          {/* Hero Section */}
          <section className="hero-section">
            <h2 className="hero-title">Get Instant Job Match Analysis</h2>
            <p className="hero-description">
              Upload your resume and job descriptions to get AI-powered
              recommendations
            </p>
          </section>

          {/* Upload Cards Grid */}
          <div className="upload-grid">
            <div className="upload-card resume-card">
              <div className="card-header">
                <div className="card-icon">📄</div>
                <h3>Upload Resume</h3>
              </div>
              <FileUpload />
            </div>

            <div className="upload-card job-card">
              <div className="card-header">
                <div className="card-icon">💼</div>
                <h3>Upload Job Description</h3>
              </div>
              <JobDescriptionUpload />
            </div>
          </div>

          {/* Future Analysis Section */}
          <section className="analysis-preview">
            <div className="preview-card">
              <h3>🔮 Coming Soon: AI Analysis</h3>
              <p>Advanced job matching and recommendations powered by AI</p>
              <div className="feature-pills">
                <span className="pill">Match Score</span>
                <span className="pill">Skills Gap</span>
                <span className="pill">Recommendations</span>
              </div>
            </div>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="modern-footer">
        <p>&copy; 2024 JobMatch AI. Powered by advanced AI technology.</p>
      </footer>
    </div>
  );
}

export default App;
