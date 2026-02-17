import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const ResultPage = () => {
  const navigate = useNavigate();
  const { state } = useLocation();

  if (!state) {
    return (
      <div style={styles.container}>
        <h2 style={{ color: "white" }}>No result data found</h2>
        <button onClick={() => navigate("/")}>Go Home</button>
      </div>
    );
  }

  const {
    candidate,
    config,
    score,
    strengths,
    improvements,
    learning_plan,
    report,
  } = state;

  // ✅ FIX: Extract domain & difficulty safely
  const domain = config?.domain || "Not Provided";
  const difficulty = config?.difficulty || "Not Provided";

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Interview Result</h1>

        <p><b>Name:</b> {candidate?.name}</p>
        <p><b>Email:</b> {candidate?.email}</p>
        <p><b>Domain:</b> {domain}</p>
        <p><b>Difficulty:</b> {difficulty}</p>

        <h2 style={styles.score}>Score: {score}/100</h2>

        {/* ✅ Strengths */}
        <h3>✅ Strengths</h3>
        <ul>
          {strengths?.length > 0 ? (
            strengths.map((s, i) => <li key={i}>{s}</li>)
          ) : (
            <li>No strengths identified</li>
          )}
        </ul>

        {/* ⚠ Improvements */}
        <h3>⚠ Areas to Improve</h3>
        <ul>
          {improvements?.length > 0 ? (
            improvements.map((i, idx) => <li key={idx}>{i}</li>)
          ) : (
            <li>No improvement areas provided</li>
          )}
        </ul>

        {/* 📘 Learning Plan */}
        <h3>📘 Personalized Learning Plan</h3>

        {learning_plan && typeof learning_plan === "object" ? (
          <>
            <p><b>Performance Level:</b> {learning_plan.performance_level}</p>

            <h4>Focus Areas</h4>
            <ul>
              {learning_plan.focus_areas?.map((f, i) => (
                <li key={i}>{f}</li>
              ))}
            </ul>

            <h4>Technical Gaps</h4>
            <ul>
              {learning_plan.technical_gaps?.map((g, i) => (
                <li key={i}>{g}</li>
              ))}
            </ul>

            <h4>2 Week Roadmap</h4>
            <ul>
              {learning_plan.two_week_roadmap?.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>

            <h4>Resources</h4>
            <ul>
              {learning_plan.recommended_resources?.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>

            <p><b>Strategy:</b> {learning_plan.improvement_strategy}</p>
          </>
        ) : (
          <p>{learning_plan}</p>
        )}

        {report && (
          <button
            style={styles.downloadBtn}
            onClick={() =>
              window.open(`http://localhost:5000/${report}`)
            }
          >
            Download Report
          </button>
        )}

        <button style={styles.homeBtn} onClick={() => navigate("/")}>
          Go Home
        </button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    minHeight: "100vh",
    background: "#020617",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: 30,
  },
  card: {
    width: "75%",
    background: "#0F172A",
    padding: 40,
    borderRadius: 16,
    color: "white",
  },
  title: { color: "#38BDF8" },
  score: { color: "#22D3EE" },
  downloadBtn: {
    marginTop: 20,
    padding: 14,
    background: "#10B981",
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
    marginRight: 10,
  },
  homeBtn: {
    marginTop: 20,
    padding: 14,
    background: "#2563EB",
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
  },
};

export default ResultPage;
