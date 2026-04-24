// SuccessPage.jsx
import React from "react";
import { useNavigate } from "react-router-dom";

const SuccessPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-green-200 to-blue-200 text-gray-800 p-6">
      <div className="bg-white rounded-2xl shadow-xl p-10 text-center max-w-lg w-full">
        <h1 className="text-4xl sm:text-5xl font-extrabold text-green-700 mb-4">
          🎉 Assessment Complete! 🎉
        </h1>
        <p className="text-xl sm:text-2xl font-semibold text-gray-700 mb-6">
          Best of luck on your career journey!
        </p>
        <p className="text-md text-gray-500 mb-8">
          You have successfully completed the assessment and reviewed your personalized roadmap.
        </p>
        <button
          onClick={() => navigate("/pilot")}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-8 rounded-full shadow-lg transition-transform transform hover:scale-105"
        >
          Return to Home
        </button>
      </div>
    </div>
  );
};

export default SuccessPage;