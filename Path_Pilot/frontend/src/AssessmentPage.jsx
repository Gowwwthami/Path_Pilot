import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Question from "./Question"; // Make sure this path is correct
import { API_BASE } from "./config";

const AssessmentPage = () => {
  const [questions, setQuestions] = useState([]);
  const [score, setScore] = useState(0);
  const [finished, setFinished] = useState(false);
  const [loading, setLoading] = useState(true); // New state for loading
  const location = useLocation();
  const selectedCareer = location?.state?.career;
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAssessment = async () => {
      if (!selectedCareer) {
        setLoading(false);
        // Handle case where no career is passed (e.g., direct URL access)
        return;
      }

      try {
        const response = await fetch(`${API_BASE}/assessment`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ career: selectedCareer }),
        });
        const data = await response.json();
        if (response.ok) {
          setQuestions(data.questions);
        } else {
          throw new Error(data.error || "Failed to fetch assessment");
        }
      } catch (error) {
        alert("Failed to load assessment: " + error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchAssessment();
  }, [selectedCareer]);

  const finishQuiz = () => {
    setFinished(true);
    // Navigate to the evaluate page, passing the score and career in the state
    navigate("/evaluate", { state: { score: score, career: selectedCareer } });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-xl text-gray-700">Loading assessment...</p>
      </div>
    );
  }

  // Handle case where selectedCareer is not defined
  if (!selectedCareer) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col">
        <h1 className="text-2xl font-bold mb-4">No Career Selected</h1>
        <p className="text-gray-600">Please go back to the home page to choose a career path.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-br from-teal-200 via-indigo-200 to-purple-200 p-6">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-3xl">
        <h1 className="text-3xl font-bold text-indigo-700 text-center">AI Assessment & Roadmap</h1>
        <h2 className="text-lg text-gray-600 text-center mt-2">
          Career: <span className="font-semibold text-purple-700">{selectedCareer}</span>
        </h2>

        <div className="mt-6 space-y-4">
          {questions.length > 0 ? (
            questions.map((q, idx) => (
              <Question
                key={idx}
                data={q}
                onAnswer={(points) => setScore((prev) => prev + points)}
              />
            ))
          ) : (
            <p className="text-center text-gray-500">
              No questions found for this career.
            </p>
          )}
        </div>

        <div className="text-center mt-6">
          <button
            onClick={finishQuiz}
            disabled={questions.length === 0 || finished}
            className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg shadow-md transition disabled:opacity-50"
          >
            Finish Assessment
          </button>
        </div>
      </div>
    </div>
  );
};

export default AssessmentPage;