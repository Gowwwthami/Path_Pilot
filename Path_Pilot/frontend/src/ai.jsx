import { useState } from "react";

export default function RoleSearch() {
  const [role, setRole] = useState("");
  const [result, setResult] = useState(null);

  const handleSearch = async () => {
    const res = await fetch("/get-role-roadmap", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role }),
    });
    const data = await res.json();
    setResult(JSON.parse(data.result));
  };

  return (
    <div className="p-4">
      <input
        type="text"
        placeholder="Enter a role (e.g., Data Scientist)"
        value={role}
        onChange={(e) => setRole(e.target.value)}
        className="border p-2 rounded"
      />
      <button
        onClick={handleSearch}
        className="ml-2 p-2 bg-blue-500 text-white rounded"
      >
        Search
      </button>

      {result && (
        <div className="mt-4">
          <h2 className="text-xl font-bold">Skills</h2>
          <ul>
            {result.skills.technical.map((s, i) => (
              <li key={i}>🔹 {s}</li>
            ))}
          </ul>
          <h2 className="text-xl font-bold mt-4">Roadmap</h2>
          {result.roadmap.map((stage, i) => (
            <div key={i} className="mt-2">
              <strong>{stage.stage}</strong>: {stage.skills.join(", ")}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}