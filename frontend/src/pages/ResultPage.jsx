import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const ResultPage = () => {
  const navigate = useNavigate();
  const { state } = useLocation();

  if (!state) {
    return (
      <div style={styles.container}>
        <h2>No result data found</h2>
        <button onClick={() => navigate("/")}>Go Home</button>
      </div>
    );
  }

  const {
    candidate,
    domain,
    difficulty,
    score,
    strengths,
    improvements,
    learning_plan,
  } = state;

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Interview Result</h1>

        <p><b>Name:</b> {candidate?.name}</p>
        <p><b>Email:</b> {candidate?.email}</p>
        <p><b>Domain:</b> {domain || "Not Provided"}</p>
        <p><b>Difficulty:</b> {difficulty || "Not Provided"}</p>

        <h2 style={styles.score}>Score: {score}/100</h2>

        {/* Strengths */}
        <h3>✅ Strengths</h3>
        <ul>
          {strengths?.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>

        {/* Improvements */}
        <h3>⚠ Areas to Improve</h3>
        <ul>
          {improvements?.map((imp, i) => (
            <li key={i}>{imp}</li>
          ))}
        </ul>

        {/* Learning Plan */}
        <h3>📘 Personalized Learning Plan</h3>

        {learning_plan && typeof learning_plan === "object" ? (
          <>
            <p><b>Performance Level:</b> {learning_plan.performance_level}</p>

            <h4>Focus Areas</h4>
            <ul>
              {learning_plan.focus_areas?.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>

            <h4>Technical Gaps</h4>
            <ul>
              {learning_plan.technical_gaps?.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>

            <h4>2 Week Roadmap</h4>
            <ul>
              {learning_plan.two_week_roadmap?.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>

            <h4>Recommended Resources</h4>
            <ul>
              {learning_plan.recommended_resources?.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>

            <p><b>Strategy:</b> {learning_plan.improvement_strategy}</p>
          </>
        ) : (
          <p>{learning_plan}</p>
        )}

        <button
          style={styles.homeBtn}
          onClick={() => navigate("/")}
        >
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