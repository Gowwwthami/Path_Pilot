// Central API base URL for PathPilot RAG System
// Override in .env with VITE_API_URL for local dev
export const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
export const API_VERSION = "/api/v1";
export const API_URL = `${API_BASE}${API_VERSION}`;
