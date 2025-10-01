import React, { useState } from "react";

interface UploadResponse {
  message: string;
  filename: string;
  original_filename: string;
  file_size: number;
  file_path: string;
  file_type: string;
}

const JobDescriptionUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string>("");

  const API_URL = "/api";

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];

      const allowedTypes = [".pdf", ".doc", ".docx", ".txt"];
      const fileExtension = selectedFile.name
        .substring(selectedFile.name.lastIndexOf("."))
        .toLowerCase();

      if (!allowedTypes.includes(fileExtension)) {
        setError(`Invalid file type. Allowed: ${allowedTypes.join(", ")}`);
        setFile(null);
        return;
      }

      if (selectedFile.size > 10 * 1024 * 1024) {
        setError("File too large. Maximum size: 10MB");
        setFile(null);
        return;
      }

      setFile(selectedFile);
      setError("");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file first");
      return;
    }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${API_URL}/upload-job-description/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Upload failed");
      }

      const data: UploadResponse = await response.json();
      setResponse(data);
      setFile(null);

      const fileInput = document.getElementById(
        "job-file-input"
      ) as HTMLInputElement;
      if (fileInput) fileInput.value = "";
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-card job-card">
      <div className="card-header">
        <div className="card-icon">💼</div>
        <h3>Upload Job Description</h3>
      </div>
      <div className="card-body">
        <div className="mb-3">
          <label htmlFor="job-file-input" className="form-label">
            Select Job Description File (PDF, DOC, DOCX, or TXT)
          </label>
          <input
            type="file"
            className="form-control"
            id="job-file-input"
            accept=".pdf,.doc,.docx,.txt"
            onChange={handleFileChange}
            disabled={loading}
          />
        </div>

        {file && (
          <div className="alert alert-info">
            <strong>Selected:</strong> {file.name} (
            {(file.size / 1024).toFixed(2)} KB)
          </div>
        )}

        {error && <div className="alert alert-danger">{error}</div>}

        {response && (
          <div className="alert alert-success">
            <h5>Upload Successful!</h5>
            <p>
              <strong>File saved as:</strong> {response.filename}
            </p>
            <p>
              <strong>Original name:</strong> {response.original_filename}
            </p>
            <p>
              <strong>Size:</strong> {(response.file_size / 1024).toFixed(2)} KB
            </p>
          </div>
        )}

        <button
          className="btn btn-success"
          onClick={handleUpload}
          disabled={!file || loading}
        >
          {loading ? (
            <>
              <span className="spinner-border spinner-border-sm me-2"></span>
              Uploading...
            </>
          ) : (
            "Upload Job Description"
          )}
        </button>
      </div>
    </div>
  );
};

export default JobDescriptionUpload;
