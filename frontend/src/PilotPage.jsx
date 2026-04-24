import React from "react";
import { useNavigate } from "react-router-dom";
import "./pages.css";

export default function PilotPage() {
  const navigate = useNavigate();

  return (
    <div className="page">
      {/* Hero */}
      <header className="hero">
        <h1 className="hero-title">
          Welcome to <span className="highlight">Path Pilot</span>
        </h1>
        <p className="hero-subtitle">
          Your co‑pilot for careers and startups. Discover roles that fit your strengths, or
          chart a practical course to build and launch your own venture.
        </p>
      </header>

      {/* Intro section */}
      <section className="section center">
        <div className="card" style={{ padding: 28 }}>
          <h2 style={{ marginTop: 0 }}>Choose your journey</h2>
          <p className="small-muted" style={{ marginBottom: 22 }}>
            Path Pilot helps you in two powerful ways. Upload a resume to get tailored career matches
            and a learning roadmap. Or explore a structured startup path with smart guidance at every stage.
          </p>
          <div className="actions">
            <button className="btn primary" onClick={() => navigate("/pilot")}>I want to find a job</button>
            <button className="btn secondary" onClick={() => navigate("/pilot/home")}>I'm building a startup</button>
          </div>
        </div>
      </section>

      {/* Benefits */}
      <section className="section">
        <div className="grid md:grid-cols-2" style={{ display: 'grid', gap: 20, gridTemplateColumns: '1fr' }}>
          <div className="card">
            <div className="brand-badge" style={{ width: 44, height: 44, marginBottom: 12 }}>
              <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5z"/>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l6.16-3.422A12.083 12.083 0 015 21.5 11.955 11.955 0 0112 14z"/>
              </svg>
            </div>
            <h3 style={{ marginTop: 0 }}>Career Compass</h3>
            <p className="muted">Upload your resume to get 5 curated roles, why they fit, and a skills roadmap with resources.</p>
          </div>
          <div className="card">
            <div className="brand-badge" style={{ width: 44, height: 44, marginBottom: 12 }}>
              <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 6h10m-8 12h6M5 10l1 10h12l1-10"/>
              </svg>
            </div>
            <h3 style={{ marginTop: 0 }}>Startup Pilot</h3>
            <p className="muted">Follow an 8‑step founder path with progress tracking and AI guidance tailored to your stage.</p>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section center">
        <div className="callout">
          <h3>Ready to get started?</h3>
          <p className="small-muted">Pick a path below — you can switch any time.</p>
          <div className="actions">
            <button className="btn primary" onClick={() => navigate("/pilot")}>Discover Career Matches</button>
            <button className="btn secondary" onClick={() => navigate("/pilot/home")}>Explore Startup Journey</button>
          </div>
        </div>
      </section>
    </div>
  );
}
