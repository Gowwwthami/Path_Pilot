import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function ProgressTracker() {
  const [user, setUser] = useState(null);
  const [completedSteps, setCompletedSteps] = useState([]);
  const [projectDetails, setProjectDetails] = useState({
    projectName: "",
    description: "",
    currentStage: "",
    challenges: "",
    goals: ""
  });
  const [isLoading, setIsLoading] = useState(false);
  const [guidance, setGuidance] = useState(null);
  const navigate = useNavigate();

  const startupSteps = [
    { id: 1, title: "Idea Validation & Market Research", icon: "💡" },
    { id: 2, title: "Business Plan & Strategy", icon: "📋" },
    { id: 3, title: "Legal & Regulatory Setup", icon: "⚖️" },
    { id: 4, title: "Funding & Investment", icon: "💰" },
    { id: 5, title: "Product Development", icon: "🚀" },
    { id: 6, title: "Marketing & Branding", icon: "📢" },
    { id: 7, title: "Team Building & Operations", icon: "👥" },
    { id: 8, title: "Launch & Growth", icon: "🎯" }
  ];

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (!userData) {
      // No login flow in this app — use a friendly guest profile
      setUser({ name: "Guest" });
    } else {
      setUser(JSON.parse(userData));
    }

    // Load saved progress
    const savedProgress = localStorage.getItem("startupProgress");
    if (savedProgress) {
      setCompletedSteps(JSON.parse(savedProgress));
    }
  }, []);

  const handleStepToggle = (stepId) => {
    setCompletedSteps(prev => {
      const newSteps = prev.includes(stepId)
        ? prev.filter(id => id !== stepId)
        : [...prev, stepId];
      
      localStorage.setItem("startupProgress", JSON.stringify(newSteps));
      return newSteps;
    });
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProjectDetails(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const getCurrentStage = () => {
    if (completedSteps.length === 0) return "Just Starting";
    if (completedSteps.length <= 2) return "Early Stage";
    if (completedSteps.length <= 5) return "Development Stage";
    if (completedSteps.length <= 7) return "Pre-Launch Stage";
    return "Growth Stage";
  };

  const handleGetGuidance = async () => {
    if (!projectDetails.projectName || !projectDetails.description) {
      alert("Please fill in at least project name and description");
      return;
    }

    setIsLoading(true);
    
    try {
      const response = await fetch("http://localhost:5000/get-startup-guidance", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          projectDetails,
          completedSteps,
          currentStage: getCurrentStage()
        }),
      });

      const data = await response.json();
      setGuidance(data);
    } catch (error) {
      console.error("Error getting guidance:", error);
      alert("Failed to get guidance. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToHome = () => {
    navigate("/pilot");
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 relative overflow-hidden">
      {/* Elegant background pattern */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/5 via-indigo-600/5 to-purple-600/5"></div>
        <div className="absolute top-0 left-0 w-full h-full opacity-40" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%236366f1' fill-opacity='0.03'%3E%3Ccircle cx='30' cy='30' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
      </div>

      {/* Header */}
      <header className="relative z-10 bg-white/80 backdrop-blur-xl border-b border-white/50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-emerald-700 rounded-xl flex items-center justify-center shadow-md">
                <svg width="24" height="24" style={{color:'#ffffff'}} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-4xl font-bold text-gray-900">
                  Progress Tracker
                </h1>
                <p className="text-gray-600 text-lg">Track your startup journey and get AI guidance</p>
              </div>
            </div>
            <button
              onClick={handleBackToHome}
              className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white px-6 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-indigo-800 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center space-x-2"
            >
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              <span>Back to Home</span>
            </button>
          </div>
        </div>
      </header>

      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Progress Tracking Section */}
          <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-gray-200">
            <div className="flex items-center space-x-3 mb-6">
              <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-emerald-700 rounded-xl flex items-center justify-center shadow-md">
                <svg width="16" height="16" style={{color:'#ffffff'}} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 className="text-3xl font-bold text-gray-900">
                Mark Completed Steps
              </h2>
            </div>
            <p className="text-gray-600 mb-8 text-lg">
              Check off the steps you've completed in your startup journey:
            </p>
            
            <div className="space-y-4">
              {startupSteps.map((step) => (
                <div
                  key={step.id}
                  className={`group flex items-center p-5 rounded-2xl border-2 transition-all duration-300 transform hover:scale-[1.02] ${
                    completedSteps.includes(step.id)
                      ? "border-green-300 bg-green-50 shadow-md"
                      : "border-gray-200 bg-gray-50 hover:border-blue-300 hover:bg-blue-50"
                  }`}
                >
                  <div className="relative">
                    <input
                      type="checkbox"
                      id={`step-${step.id}`}
                      checked={completedSteps.includes(step.id)}
                      onChange={() => handleStepToggle(step.id)}
                      className="h-6 w-6 text-green-600 focus:ring-green-500 border-gray-300 rounded-lg bg-white"
                    />
                    {completedSteps.includes(step.id) && (
                      <div className="absolute inset-0 flex items-center justify-center">
                        <svg width="14" height="14" className="text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                    )}
                  </div>
                  <label
                    htmlFor={`step-${step.id}`}
                    className="ml-5 flex items-center cursor-pointer flex-1 group-hover:text-gray-800 transition-colors duration-300"
                  >
                    <span style={{fontSize: '22px', lineHeight: 1, color: '#4b6cb7'}} className="mr-4">
                      {step.icon}
                    </span>
                    <div>
                      <div className={`font-bold text-lg ${
                        completedSteps.includes(step.id) 
                          ? "text-green-800" 
                          : "text-gray-800 group-hover:text-blue-700"
                      }`}>
                        Step {step.id}: {step.title}
                      </div>
                    </div>
                  </label>
                </div>
              ))}
            </div>
            
            <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl border border-blue-200">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-indigo-700 rounded-lg flex items-center justify-center shadow-md">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
                <h3 className="font-bold text-gray-800 text-lg">Current Stage:</h3>
              </div>
              <p className="text-blue-700 text-xl font-semibold mb-2">{getCurrentStage()}</p>
              <div className="flex items-center justify-between">
                <p className="text-blue-600 text-sm">
                  Completed: {completedSteps.length} of {startupSteps.length} steps
                </p>
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-gradient-to-r from-blue-600 to-indigo-700 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${(completedSteps.length / startupSteps.length) * 100}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Project Details & Guidance Section */}
          <div className="space-y-8">
            {/* Project Details Form */}
            <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-gray-200">
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-10 h-10 bg-gradient-to-br from-purple-600 to-indigo-700 rounded-xl flex items-center justify-center shadow-md">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <h2 className="text-3xl font-bold text-gray-900">
                  Tell Us About Your Project
                </h2>
              </div>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Project Name *
                  </label>
                  <input
                    type="text"
                    name="projectName"
                    value={projectDetails.projectName}
                    onChange={handleInputChange}
                    className="w-full px-4 py-4 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-300 hover:border-gray-300"
                    placeholder="Enter your startup/project name"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Project Description *
                  </label>
                  <textarea
                    name="description"
                    value={projectDetails.description}
                    onChange={handleInputChange}
                    rows={4}
                    className="w-full px-4 py-4 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-300 hover:border-gray-300 resize-none"
                    placeholder="Describe your project, what problem it solves, and your target market"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Current Stage
                  </label>
                  <select
                    name="currentStage"
                    value={projectDetails.currentStage}
                    onChange={handleInputChange}
                    className="w-full px-4 py-4 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-300 hover:border-gray-300"
                  >
                    <option value="">Select current stage</option>
                    <option value="idea">Just an idea</option>
                    <option value="validation">Validating idea</option>
                    <option value="development">Developing product</option>
                    <option value="testing">Testing with users</option>
                    <option value="launch">Ready to launch</option>
                    <option value="growth">Growing business</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Current Challenges
                  </label>
                  <textarea
                    name="challenges"
                    value={projectDetails.challenges}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-4 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-300 hover:border-gray-300 resize-none"
                    placeholder="What challenges are you facing right now?"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-3">
                    Goals
                  </label>
                  <textarea
                    name="goals"
                    value={projectDetails.goals}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-4 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 transition-all duration-300 hover:border-gray-300 resize-none"
                    placeholder="What are your short-term and long-term goals?"
                  />
                </div>
              </div>
              
              <button
                onClick={handleGetGuidance}
                disabled={isLoading || !projectDetails.projectName || !projectDetails.description}
                className="w-full mt-8 bg-gradient-to-r from-purple-600 to-indigo-700 text-white py-4 px-6 rounded-xl font-bold hover:from-purple-700 hover:to-indigo-800 focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 shadow-lg hover:shadow-xl"
              >
                {isLoading ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-white mr-3"></div>
                    <span className="text-lg">Getting AI Guidance...</span>
                  </div>
                ) : (
                  <div className="flex items-center justify-center">
                    <svg width="24" height="24" style={{marginRight:'12px'}} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                    <span className="text-lg">Get AI Guidance</span>
                  </div>
                )}
              </button>
            </div>

            {/* AI Guidance Results */}
            {guidance && (
              <div className="bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-8 border border-gray-200">
                <div className="flex items-center space-x-3 mb-6">
                  <div className="w-10 h-10 bg-gradient-to-br from-yellow-500 to-orange-600 rounded-xl flex items-center justify-center shadow-md">
                    <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <h2 className="text-3xl font-bold text-gray-900">
                    🤖 AI Guidance
                  </h2>
                </div>
                <div className="prose max-w-none text-gray-700">
                  <div 
                    className="bg-gray-50 rounded-xl p-6 border border-gray-200"
                    dangerouslySetInnerHTML={{ __html: guidance.guidance }} 
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
