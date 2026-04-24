import React, { useState } from "react";

const Question = ({ data, onAnswer }) => {
  const [input, setInput] = useState("");
  const [selected, setSelected] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [answered, setAnswered] = useState(false);

  const checkMCQ = (index) => {
    if (answered) return;
    setSelected(index);
    if (index === data.answer) {
      setFeedback("✅ Correct!");
      onAnswer(data.points);
    } else {
      setFeedback("❌ Wrong. Correct: " + data.options[data.answer]);
      onAnswer(0);
    }
    setAnswered(true);
  };

  const checkFill = () => {
    if (answered) return;
    if (input.trim().toLowerCase() === data.answer.toLowerCase()) {
      setFeedback("✅ Correct!");
      onAnswer(data.points);
    } else {
      setFeedback("❌ Wrong. Correct: " + data.answer);
      onAnswer(0);
    }
    setAnswered(true);
  };

  return (
    <div className="p-6 border rounded-xl shadow-md bg-white">
      <h2 className="font-semibold text-lg text-gray-800">{data.question}</h2>

      {data.type === "mcq" && (
        <div className="mt-3 space-y-2">
          {data.options.map((opt, i) => (
            <button
              key={i}
              onClick={() => checkMCQ(i)}
              disabled={answered}
              className={`w-full text-left px-4 py-2 rounded-lg transition ${
                selected === i ? "bg-indigo-300" : "bg-gray-100 hover:bg-indigo-100"
              }`}
            >
              {opt}
            </button>
          ))}
        </div>
      )}

      {data.type === "fill" && (
        <div className="mt-4">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={answered}
            className="border p-2 rounded w-full focus:outline-none focus:ring focus:ring-indigo-300"
            placeholder="Type your answer"
          />
          <button
            onClick={checkFill}
            disabled={answered}
            className="mt-3 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow transition"
          >
            Submit
          </button>
        </div>
      )}

      {feedback && (
        <p
          className={`mt-3 font-medium ${
            feedback.startsWith("✅") ? "text-green-600" : "text-red-600"
          }`}
        >
          {feedback}
        </p>
      )}
    </div>
  );
};

export default Question;
