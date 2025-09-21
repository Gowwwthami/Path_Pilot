import { StrictMode } from "react";
import "@fortawesome/fontawesome-free/css/all.css";
import { createRoot } from "react-dom/client";
import "./theme.css"; // global theme (no Tailwind)
import "./index.css";
import App from "./App.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
