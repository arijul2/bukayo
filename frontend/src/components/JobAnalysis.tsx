import React, { useState, useEffect } from "react";

interface FileInfo {
  filename: string;
  size: number;
  created: number;
  type: string;
}

interface AnalysisResult {
  recommendation: string;
  match_score: number;
  confidence_score: number;
  strengths: string[];
  weaknesses: string[];
  missing_skills: string[];
  experience_match: string;
  education_match: string;
  detailed_reasoning: string;
  analysis_timestamp: string;
  ai_model: string;
  processing_status: string;
}

const JobAnalysis: React.FC = () => {
  const [resumes, setResumes] = useState<FileInfo[]>([]);
  const [jobDescriptions, setJobDescriptions] = useState<FileInfo[]>([]);
  const [selectedResume, setSelectedResume] = useState<string>("");
  const [selectedJob, setSelectedJob] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string>("");

  const API_URL = "/api";

  // Fetch uploaded files on component mount
  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      // Fetch resumes
      const resumeResponse = await fetch(`${API_URL}/resumes/`);
      const resumeData = await resumeResponse.json();
      setResumes(resumeData.resumes || []);

      // Fetch job descriptions
      const jobResponse = await fetch(`${API_URL}/job-descriptions/`);
      const jobData = await jobResponse.json();
      setJobDescriptions(jobData.job_descriptions || []);
    } catch (err) {
      console.error("Failed to fetch files:", err);
    }
  };

  const analyzeJobMatch = async () => {
    if (!selectedResume || !selectedJob) {
      setError("Please select both a resume and job description");
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const formData = new FormData();
      formData.append("resume_filename", selectedResume);
      formData.append("job_filename", selectedJob);

      const response = await fetch(`${API_URL}/analyze-job-match/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Analysis failed");
      }

      const data = await response.json();
      setAnalysis(data.analysis);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const getRecommendationColor = (recommendation: string) => {
    switch (recommendation) {
      case "APPLY":
        return "success";
      case "DECENT_CHANCE":
        return "warning";
      case "AVOID":
        return "danger";
      default:
        return "secondary";
    }
  };

  const getRecommendationIcon = (recommendation: string) => {
    switch (recommendation) {
      case "APPLY":
        return "🎯";
      case "DECENT_CHANCE":
        return "🤔";
      case "AVOID":
        return "❌";
      default:
        return "📊";
    }
  };

  return (
    <div className="container mt-4">
      <div className="card analysis-card">
        <div className="card-header bg-gradient-primary text-white">
          <div className="d-flex align-items-center">
            <span className="analysis-icon me-2">🧠</span>
            <h3 className="mb-0">AI Job Match Analysis</h3>
          </div>
        </div>

        <div className="card-body">
          {/* File Selection */}
          <div className="row mb-4">
            <div className="col-md-6">
              <label className="form-label fw-bold">Select Resume:</label>
              <select
                className="form-select"
                value={selectedResume}
                onChange={(e) => setSelectedResume(e.target.value)}
                disabled={loading}
              >
                <option value="">Choose a resume...</option>
                {resumes.map((resume) => (
                  <option key={resume.filename} value={resume.filename}>
                    {resume.filename.substring(0, 20)}... (
                    {(resume.size / 1024).toFixed(1)}KB)
                  </option>
                ))}
              </select>
            </div>

            <div className="col-md-6">
              <label className="form-label fw-bold">
                Select Job Description:
              </label>
              <select
                className="form-select"
                value={selectedJob}
                onChange={(e) => setSelectedJob(e.target.value)}
                disabled={loading}
              >
                <option value="">Choose a job description...</option>
                {jobDescriptions.map((job) => (
                  <option key={job.filename} value={job.filename}>
                    {job.filename.substring(0, 20)}... (
                    {(job.size / 1024).toFixed(1)}KB)
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Analyze Button */}
          <div className="text-center mb-4">
            <button
              className="btn btn-primary btn-lg analyze-btn"
              onClick={analyzeJobMatch}
              disabled={!selectedResume || !selectedJob || loading}
            >
              {loading ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2"></span>
                  Analyzing with AI...
                </>
              ) : (
                <>
                  <span className="me-2">🚀</span>
                  Analyze Job Match
                </>
              )}
            </button>
          </div>

          {/* Error Display */}
          {error && (
            <div className="alert alert-danger">
              <strong>Analysis Failed:</strong> {error}
            </div>
          )}

          {/* Analysis Results */}
          {analysis && (
            <div className="analysis-results">
              {/* Recommendation Header */}
              <div
                className={`alert alert-${getRecommendationColor(
                  analysis.recommendation
                )} recommendation-alert`}
              >
                <div className="d-flex align-items-center justify-content-between">
                  <div className="d-flex align-items-center">
                    <span className="recommendation-icon me-3">
                      {getRecommendationIcon(analysis.recommendation)}
                    </span>
                    <div>
                      <h4 className="mb-1">
                        Recommendation:{" "}
                        {analysis.recommendation.replace("_", " ")}
                      </h4>
                      <p className="mb-0">
                        Match Score: {analysis.match_score}% | Confidence:{" "}
                        {analysis.confidence_score}%
                      </p>
                    </div>
                  </div>
                  <div className="score-circle">
                    <span className="score-text">{analysis.match_score}%</span>
                  </div>
                </div>
              </div>

              {/* Detailed Analysis */}
              <div className="row">
                <div className="col-md-6">
                  <div className="analysis-section">
                    <h5 className="text-success">💪 Strengths</h5>
                    <ul className="list-unstyled">
                      {analysis.strengths.map((strength, index) => (
                        <li key={index} className="mb-2">
                          <span className="badge bg-success me-2">✓</span>
                          {strength}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="analysis-section mt-4">
                    <h5 className="text-info">🎓 Education Match</h5>
                    <p className="analysis-text">{analysis.education_match}</p>
                  </div>
                </div>

                <div className="col-md-6">
                  <div className="analysis-section">
                    <h5 className="text-warning">⚠️ Areas for Improvement</h5>
                    <ul className="list-unstyled">
                      {analysis.weaknesses.map((weakness, index) => (
                        <li key={index} className="mb-2">
                          <span className="badge bg-warning me-2">!</span>
                          {weakness}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="analysis-section mt-4">
                    <h5 className="text-primary">💼 Experience Match</h5>
                    <p className="analysis-text">{analysis.experience_match}</p>
                  </div>
                </div>
              </div>

              {/* Missing Skills */}
              {analysis.missing_skills.length > 0 && (
                <div className="analysis-section mt-4">
                  <h5 className="text-danger">🔧 Missing Skills</h5>
                  <div className="missing-skills">
                    {analysis.missing_skills.map((skill, index) => (
                      <span
                        key={index}
                        className="badge bg-light text-dark me-2 mb-2 skill-badge"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Detailed Reasoning */}
              <div className="analysis-section mt-4">
                <h5 className="text-dark">📝 Detailed Analysis</h5>
                <div className="reasoning-box">
                  <p className="analysis-text">{analysis.detailed_reasoning}</p>
                </div>
              </div>

              {/* Metadata */}
              <div className="analysis-metadata mt-4 pt-3 border-top">
                <small className="text-muted">
                  Analysis powered by {analysis.ai_model} • Generated on{" "}
                  {new Date(analysis.analysis_timestamp).toLocaleString()}
                </small>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default JobAnalysis;
