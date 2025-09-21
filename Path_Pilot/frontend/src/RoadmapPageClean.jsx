// RoadmapPageClean.jsx
import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { API_BASE } from "./config";

function RoadmapPage() {
  const location = useLocation();
  const { score, career } = location.state || { score: 0, career: "Software Engineer" };
  const navigate = useNavigate();
  const [language, setLanguage] = useState("Python");
  const [roadmap, setRoadmap] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [rawJsonVisible, setRawJsonVisible] = useState(false);
  const [openPhases, setOpenPhases] = useState({});

  const togglePhase = (idx) => {
    setOpenPhases((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const fetchRoadmap = async () => {
    setError(null);
    setRoadmap(null);
    setLoading(true);

    const numericScore = parseInt(score || "0", 10);

    try {
      const res = await fetch(`${API_BASE}/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ score: numericScore, career, language }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(
          data.error ? `${data.error} - check raw_text in debug output` : `Server returned ${res.status}`
        );
        setRoadmap(data);
        setRawJsonVisible(true);
      } else {
        setRoadmap(data);
      }
    } catch (err) {
      setError("Network or parsing error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const renderQuizQuestion = (q, pIdx, tIdx, qIdx) => {
    if (!q || !q.type) return null;
    if (q.type === "mcq") {
      const options = q.options || [];
      return (
        <div className="my-2">
          <p className="font-medium">{q.question}</p>
          {options.map((opt, i) => (
            <label key={i} className="block">
              <input type="radio" name={`q-${pIdx}-${tIdx}-${qIdx}`} /> {opt}
            </label>
          ))}
        </div>
      );
    }
    if (q.type === "fill") {
      return (
        <div className="my-2">
          <p className="font-medium">{q.question}</p>
          <input type="text" placeholder="Your answer" className="border p-1 w-full" />
        </div>
      );
    }
    if (q.type === "code") {
      return (
        <div className="my-2">
          <p className="font-medium">{q.question}</p>
          <textarea placeholder="Write code..." rows={6} className="border p-2 w-full" />
        </div>
      );
    }
    return null;
  };

  const finishroadmap = () => {
    navigate("/success");
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">AI Assessment & Roadmap</h1>

      <div className="mb-4 grid grid-cols-1 md:grid-cols-3 gap-2">
        <input
          type="number"
          min="0"
          max="10"
          value={score}
          onChange={(e) => setScore(e.target.value)}
          placeholder="Score (0-10)"
          className="border p-2"
        />
        <input
          type="text"
          value={career}
          onChange={(e) => setCareer(e.target.value)}
          placeholder="Career role (e.g. Backend Engineer)"
          className="border p-2"
        />
        <input
          type="text"
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          placeholder="Preferred language (Python, Java, JS...)"
          className="border p-2"
        />
      </div>

      <div className="mb-4">
        <button
          onClick={fetchRoadmap}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-60"
        >
          {loading ? "Generating roadmap..." : "Get Roadmap"}
        </button>
        {error && <div className="text-red-600 mt-2">{error}</div>}
      </div>

      {roadmap && (
        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">
            🚀 {roadmap.career || career} Roadmap (Score: {roadmap.score ?? score})
          </h2>

          {roadmap.raw_text && (
            <div className="bg-yellow-100 p-3 border mb-4">
              <strong>Debug: server returned raw model text (parsing failed)</strong>
              <pre className="whitespace-pre-wrap">{roadmap.raw_text}</pre>
            </div>
          )}

          {Array.isArray(roadmap.roadmap) && roadmap.roadmap.length > 0 ? (
            roadmap.roadmap.map((phase, pIdx) => (
              <div key={pIdx} className="mb-4 border rounded overflow-hidden">
                <div
                  className="p-3 bg-gray-200 cursor-pointer"
                  onClick={() => togglePhase(pIdx)}
                >
                  <h3 className="font-bold">{phase.phase || `Phase ${pIdx + 1}`}</h3>
                </div>

                {openPhases[pIdx] && (
                  <div className="p-4 bg-white">
                    {Array.isArray(phase.topics) && phase.topics.length > 0 ? (
                      phase.topics.map((topic, tIdx) => (
                        <div key={tIdx} className="mb-4 p-3 border rounded bg-gray-50">
                          <h4 className="font-bold">{topic.title || `Topic ${tIdx + 1}`}</h4>

                          <div className="mt-2">
                            <p className="font-semibold">🎥 Video Resources (Top 5)</p>
                            <ul className="list-disc ml-6">
                              {(topic.video_resources || []).map((v, i) => (
                                <li key={i}>
                                  {v.link ? (
                                    <a href={v.link} target="_blank" rel="noreferrer" className="text-blue-600 underline">
                                      {v.name || v.link}
                                    </a>
                                  ) : (
                                    <span>{v.name || "(no link provided)"}</span>
                                  )}
                                </li>
                              ))}
                              {!(topic.video_resources || []).length && <li>(none)</li>}
                            </ul>
                          </div>

                          <div className="mt-2">
                            <p className="font-semibold">📖 Book / Article Resources</p>
                            <ul className="list-disc ml-6">
                              {(topic.book_resources || []).map((b, i) => (
                                <li key={i}>
                                  {b.link ? (
                                    <a href={b.link} target="_blank" rel="noreferrer" className="text-green-600 underline">
                                      {b.name || b.link}
                                    </a>
                                  ) : (
                                    <span>{b.name || "(no link provided)"}</span>
                                  )}
                                </li>
                              ))}
                              {!(topic.book_resources || []).length && <li>(none)</li>}
                            </ul>
                          </div>

                          <div className="mt-2">
                            <p className="font-semibold">📝 Quiz (topic-specific)</p>
                            {Array.isArray(topic.quiz) && topic.quiz.length > 0 ? (
                              topic.quiz.map((q, qIdx) => (
                                <div key={qIdx} className="mt-2">
                                  {renderQuizQuestion(q, pIdx, tIdx, qIdx)}
                                </div>
                              ))
                            ) : (
                              <div className="text-sm text-gray-500">No quiz provided.</div>
                            )}
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="text-sm text-gray-600">No topics provided in this phase.</div>
                    )}
                  </div>
                )}
              </div>
            ))
          ) : (
            <div className="text-sm text-gray-600">No roadmap returned. Toggle raw JSON to debug.</div>
          )}

          <div className="text-center mt-8">
            <button
              onClick={finishroadmap}
              className="bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg shadow-lg font-semibold transition-transform transform hover:scale-105"
            >
              Finish & Conclude Assessment
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default RoadmapPage;
