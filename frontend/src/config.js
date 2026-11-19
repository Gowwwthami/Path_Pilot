// Central API base URL for PathPilot RAG System
// Override with VITE_API_URL (e.g. your Render backend URL)
export const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5000";
export const API_VERSION = "/api/v1";
export const API_URL = `${API_BASE}${API_VERSION}`;
