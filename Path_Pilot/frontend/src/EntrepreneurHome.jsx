import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function EntrepreneurHome() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (!userData) {
      // No login in this app — fall back to a friendly guest user
      setUser({ name: "Guest" });
      return;
    }
    setUser(JSON.parse(userData));
  }, []);

  const startupSteps = [
    {
      id: 1,
      title: "Idea Validation & Market Research",
      description: "Validate your business idea through market research, customer interviews, and competitive analysis.",
      details: [
        "Conduct customer interviews and surveys",
        "Analyze market size and competition",
        "Create a value proposition canvas",
        "Test your minimum viable product (MVP) concept"
      ],
      icon: "💡"
    },
    {
      id: 2,
      title: "Business Plan & Strategy",
      description: "Develop a comprehensive business plan including financial projections and go-to-market strategy.",
      details: [
        "Write a detailed business plan",
        "Create financial projections and budgets",
        "Define your target market and customer personas",
        "Develop pricing strategy and revenue models"
      ],
      icon: "📋"
    },
    {
      id: 3,
      title: "Legal & Regulatory Setup",
      description: "Establish your business legally with proper registrations, licenses, and compliance requirements.",
      details: [
        "Choose business structure (LLC, Corporation, etc.)",
        "Register your business name and domain",
        "Obtain necessary licenses and permits",
        "Set up business bank accounts and accounting"
      ],
      icon: "⚖️"
    },
    {
      id: 4,
      title: "Funding & Investment",
      description: "Secure funding through various channels including bootstrapping, investors, or loans.",
      details: [
        "Bootstrap with personal savings",
        "Apply for business loans or grants",
        "Pitch to angel investors or VCs",
        "Consider crowdfunding platforms"
      ],
      icon: "💰"
    },
    {
      id: 5,
      title: "Product Development",
      description: "Build and develop your product or service with focus on quality and user experience.",
      details: [
        "Develop your MVP (Minimum Viable Product)",
        "Implement user feedback and iterations",
        "Ensure quality assurance and testing",
        "Prepare for product launch"
      ],
      icon: "🚀"
    },
    {
      id: 6,
      title: "Marketing & Branding",
      description: "Create a strong brand identity and marketing strategy to reach your target audience.",
      details: [
        "Develop brand identity and logo",
        "Create marketing materials and website",
        "Implement digital marketing strategies",
        "Build social media presence"
      ],
      icon: "📢"
    },
    {
      id: 7,
      title: "Team Building & Operations",
      description: "Hire the right team and establish operational processes for sustainable growth.",
      details: [
        "Define roles and responsibilities",
        "Hire key team members",
        "Establish company culture and values",
        "Set up operational processes and workflows"
      ],
      icon: "👥"
    },
    {
      id: 8,
      title: "Launch & Growth",
      description: "Launch your business and focus on growth, customer acquisition, and scaling operations.",
      details: [
        "Execute product launch strategy",
        "Focus on customer acquisition",
        "Monitor key performance indicators",
        "Plan for scaling and expansion"
      ],
      icon: "🎯"
    }
  ];

  const handleGetStarted = () => {
    navigate("/pilot/progress-tracker");
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    // Stay on this page and switch to guest view instead of navigating
    setUser({ name: "Guest" });
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
              <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-xl flex items-center justify-center shadow-lg">
                <svg width="24" height="24" style={{color:'#ffffff'}} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <div>
                <h1 className="text-4xl font-bold text-gray-900">
                  Startup Journey
                </h1>
                <p className="text-gray-600 text-lg">Welcome back, {user.name}! 🚀</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="bg-gradient-to-r from-red-500 to-red-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-red-600 hover:to-red-700 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl flex items-center space-x-2"
            >
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-16">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl mb-8 shadow-lg">
            <svg width="40" height="40" style={{color:'#ffffff'}} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-5xl font-bold text-gray-900 mb-6">
            Your Path to Startup Success
          </h2>
          <p className="text-xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
            Follow these essential steps to build a successful startup from idea to launch and beyond. 
            Each step is designed to guide you through the entrepreneurial journey with confidence.
          </p>
        </div>

        {/* Steps Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {startupSteps.map((step, index) => (
            <div
              key={step.id}
              className="group bg-white/90 backdrop-blur-sm rounded-2xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 hover:scale-105 border border-gray-200 hover:border-blue-300 relative overflow-hidden"
              style={{ animationDelay: `${index * 100}ms` }}
            >
              {/* Gradient overlay */}
              <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 via-indigo-50/50 to-purple-50/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              
              <div className="relative z-10">
                <div className="text-center mb-6">
                  <div className="mb-4" style={{fontSize: '28px', lineHeight: 1, color: '#4b6cb7'}}>
                    {step.icon}
                  </div>
                  <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white text-sm font-bold px-4 py-2 rounded-full inline-block mb-4 shadow-md">
                    Step {step.id}
                  </div>
                  <h3 className="text-xl font-bold text-gray-900 mb-3 group-hover:text-blue-700 transition-colors duration-300">
                    {step.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-6 leading-relaxed">
                    {step.description}
                  </p>
                </div>
                
                <div className="space-y-3">
                  <h4 className="font-bold text-gray-800 text-sm mb-3 flex items-center">
                    <svg width="16" height="16" style={{color:'#2563eb', marginRight: '8px'}} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                    Key Activities:
                  </h4>
                  <ul className="text-xs text-gray-600 space-y-2">
                    {step.details.map((detail, detailIndex) => (
                      <li key={detailIndex} className="flex items-start group-hover:text-gray-800 transition-colors duration-300">
                        <span className="text-blue-600 mr-3 mt-1 flex-shrink-0">▶</span>
                        <span className="leading-relaxed">{detail}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="relative text-center bg-white/90 backdrop-blur-sm rounded-3xl shadow-2xl p-12 border border-gray-200 overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 bg-gradient-to-r from-blue-50/50 via-indigo-50/50 to-purple-50/50"></div>
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600"></div>
          
          <div className="relative z-10">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl mb-8 shadow-lg">
              <svg width="32" height="32" style={{color:'#ffffff'}} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="text-4xl font-bold text-gray-900 mb-6">
              Ready to Track Your Progress?
            </h3>
            <p className="text-xl text-gray-600 mb-10 max-w-3xl mx-auto leading-relaxed">
              Let's assess where you are in your startup journey and get personalized guidance 
              based on your current progress and project details. Our AI will provide tailored 
              recommendations to help you succeed.
            </p>
            <button
              onClick={handleGetStarted}
              className="group bg-gradient-to-r from-blue-600 to-indigo-700 text-white px-10 py-5 rounded-2xl text-xl font-bold hover:from-blue-700 hover:to-indigo-800 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl shadow-xl flex items-center mx-auto space-x-3"
            >
              <span>Track My Progress</span>
              <svg width="24" height="24" className="group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
