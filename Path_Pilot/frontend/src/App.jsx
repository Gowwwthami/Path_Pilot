import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CareerAdvisorFrontend from "./CareerAdvisorFrontend";
import AssessmentPage from "./AssessmentPage";
import RoadmapPage from './RoadmapPage';
import SuccessPage from "./SuccessPage";
import EntrepreneurHome from "./EntrepreneurHome";
import ProgressTracker from "./ProgressTracker";
import TestTailwind from "./TestTailwind";
import Ai from "./ai";
import Layout from "./Layout";
import PilotPage from "./PilotPage";

function App() {
  return (
    <Router>
      <Routes>
      <Route path="/" element={<PilotPage />} />
        <Route path="/pilot" element={<Layout />}>
          <Route index element={<CareerAdvisorFrontend />} />
          
          <Route path="assessment" element={<AssessmentPage />} />
          <Route path="evaluate" element={<RoadmapPage />} /> 
          <Route path="success" element={<SuccessPage />} />
          <Route path="home" element={<EntrepreneurHome />} />
          <Route path="progress-tracker" element={<ProgressTracker />} />
          <Route path="test" element={<TestTailwind />} />
          <Route path="ai" element={<Ai />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
