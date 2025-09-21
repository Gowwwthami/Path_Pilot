import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import * as pdfjsLib from "pdfjs-dist/build/pdf";
import workerUrl from "pdfjs-dist/build/pdf.worker.js?url";
import "./CareerAdvisorFrontend.css"; // Import the CSS

// Set PDF.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = workerUrl;

const CareerAdvisorFrontend = () => {
  const [resumeText, setResumeText] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Extract text from PDF
  const extractPdfText = async (file) => {
    const arrayBuffer = await file.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
    let text = "";
    for (let i = 1; i <= pdf.numPages; i++) {
      const page = await pdf.getPage(i);
      const content = await page.getTextContent();
      text += content.items.map((item) => item.str).join(" ") + " ";
    }
    return text.trim();
  };

  // Handle PDF upload
  const handleResumeUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.type === "application/pdf") {
      try {
        setLoading(true);
        const text = await extractPdfText(file);
        if (!text) throw new Error("Empty PDF or scanned document");
        setResumeText(text);
      } catch (err) {
        console.error("PDF extraction failed:", err);
        alert("Could not read the PDF file. Please try another resume.");
      } finally {
        setLoading(false);
      }
    } else {
      alert("Only PDF resumes are supported.");
    }
  };

  // Submit resume to backend
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!resumeText) return alert("Please upload a resume first.");

    setLoading(true);
    setRecommendations([]);
    try {
      const response = await fetch("http://localhost:5000/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume: resumeText }),
      });

      if (!response.ok) throw new Error("Backend error");

      const data = await response.json();
      setRecommendations(data.recommendations || []);
    } catch (err) {
      console.error(err);
      alert("Could not connect to backend. Make sure the server is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="career-compass-container">
      {/* Hero Section */}
      <header className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Discover Your <span className="highlight">Perfect Career</span> Path
          </h1>
          <p className="hero-subtitle">
            Upload your resume and let our AI analyze your skills to match you with careers where you'll excel.
          </p>
        </div>
      </header>

      {/* Upload Section */}
      <section className="upload-section">
        <div className="section-container">
          <h2 className="section-title">Upload Your Resume</h2>
          <form onSubmit={handleSubmit} className="upload-form">
            <input
              type="file"
              id="resume-upload"
              accept=".pdf"
              onChange={handleResumeUpload}
              className="file-input"
            />
            <label htmlFor="resume-upload" className="file-upload-label">
              {resumeText ? "Resume Uploaded ✅" : "Click to upload your PDF resume"}
            </label>
            <button type="submit" className="cta-button" disabled={loading || !resumeText}>
              {loading ? "Analyzing..." : "Discover My Career Matches"}
            </button>
          </form>
        </div>
      </section>

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <section className="results-section">
          <div className="section-container">
            <h2>Your Career Matches</h2>
            <div className="career-grid">
              {recommendations.map((job, idx) => (
                <div key={idx} className="career-card">
                  <div className="card-header">
                    <h3>{job.title}</h3>
                    <span className="match-badge">{job.rank}% Match</span>
                  </div>
                  <div className="card-body">
                    <h4>Why you're a great fit:</h4>
                    <ul>
                      {job.why_fit.map((reason, i) => (
                        <li key={i}>✔️ {reason}</li>
                      ))}
                    </ul>
                  </div>
                  <div className="card-footer">
                    <button
                      className="assessment-button"
                      onClick={() =>
                        navigate("/assessment", { state: { career: job.title } })
                      }
                    >
                      Take Skill Assessment →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default CareerAdvisorFrontend;
