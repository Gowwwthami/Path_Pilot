import React from "react";
import { NavLink, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100">
      {/* Top Nav */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-xl border-b border-white/50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-lg flex items-center justify-center shadow">
                <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <span className="text-xl font-bold text-gray-900">Path Pilot</span>
            </div>
            <div className="hidden md:flex items-center space-x-2">
              <NavLink to="/pilot" className={({isActive}) => `px-3 py-2 rounded-lg text-sm font-semibold ${isActive ? 'text-white bg-blue-600' : 'text-gray-700 hover:text-blue-700 hover:bg-blue-50'}`}>Home</NavLink>
              <NavLink to="/assessment" className={({isActive}) => `px-3 py-2 rounded-lg text-sm font-semibold ${isActive ? 'text-white bg-blue-600' : 'text-gray-700 hover:text-blue-700 hover:bg-blue-50'}`}>Assessment</NavLink>
              <NavLink to="/evaluate" className={({isActive}) => `px-3 py-2 rounded-lg text-sm font-semibold ${isActive ? 'text-white bg-blue-600' : 'text-gray-700 hover:text-blue-700 hover:bg-blue-50'}`}>Roadmap</NavLink>
              <NavLink to="/home" className={({isActive}) => `px-3 py-2 rounded-lg text-sm font-semibold ${isActive ? 'text-white bg-blue-600' : 'text-gray-700 hover:text-blue-700 hover:bg-blue-50'}`}>Startup</NavLink>
              <NavLink to="/progress-tracker" className={({isActive}) => `px-3 py-2 rounded-lg text-sm font-semibold ${isActive ? 'text-white bg-blue-600' : 'text-gray-700 hover:text-blue-700 hover:bg-blue-50'}`}>Progress</NavLink>
              <NavLink to="/ai" className={({isActive}) => `px-3 py-2 rounded-lg text-sm font-semibold ${isActive ? 'text-white bg-blue-600' : 'text-gray-700 hover:text-blue-700 hover:bg-blue-50'}`}>AI</NavLink>
              <NavLink to="/test" className={({isActive}) => `px-3 py-2 rounded-lg text-sm font-semibold ${isActive ? 'text-white bg-blue-600' : 'text-gray-700 hover:text-blue-700 hover:bg-blue-50'}`}>Style</NavLink>
            </div>
          </div>
        </div>
      </nav>

      {/* Page content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="mt-10 border-t bg-white/70 backdrop-blur-xl border-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-sm text-gray-600 flex flex-col sm:flex-row items-center justify-between">
          <span>© {new Date().getFullYear()} Path Pilot. All rights reserved.</span>
          <span className="mt-2 sm:mt-0">Built with ❤️ using React & TailwindCSS</span>
        </div>
      </footer>
    </div>
  );
}
