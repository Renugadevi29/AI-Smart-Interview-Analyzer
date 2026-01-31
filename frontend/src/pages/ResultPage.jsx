import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const ResultPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const result = location.state;

  if (!result) {
    return (
      <div style={styles.container}>
        <h2 style={{ color: "red" }}>No result data found</h2>
        <button onClick={() => navigate("/")}>Go Home</button>
      </div>
    );
  }

  const {
    candidate,
    score,
    strengths,
    improvements,
    learning_plan,
    report,
  } = result;

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Interview Result</h1>

        <p><b>Name:</b> {candidate?.name}</p>
        <p><b>Email:</b> {candidate?.email}</p>

        <h2 style={styles.score}>Score: {score}/10</h2>

        <section>
          <h3>✅ Strengths</h3>
          <ul>
            {strengths?.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </section>

        <section>
          <h3>⚠️ Areas to Improve</h3>
          <ul>
            {improvements?.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </section>

        <section>
          <h3>📘 Personalized Learning Plan</h3>

          {typeof learning_plan === "string" ? (
            <p>{learning_plan}</p>
          ) : (
            Object.entries(learning_plan).map(([key, value], i) => (
              <div key={i} style={{ marginBottom: 12 }}>
                <h4>{key}</h4>
                <p>{value}</p>
              </div>
            ))
          )}
        </section>

        <button
          style={styles.downloadBtn}
          onClick={() => window.open(`http://localhost:5000/${report}`)}
        >
          📥 Download Interview Report
        </button>

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
    background: "#020617",
    color: "white",
    padding: 30,
    borderRadius: 16,
    width: "70%",
    boxShadow: "0 0 30px rgba(37,99,235,0.25)",
  },
  title: {
    color: "#38BDF8",
    marginBottom: 10,
  },
  score: {
    color: "#22D3EE",
    marginTop: 15,
  },
  downloadBtn: {
    marginTop: 20,
    padding: 14,
    background: "#10B981",
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
    fontWeight: "bold",
    marginRight: 10,
  },
  homeBtn: {
    marginTop: 20,
    padding: 14,
    background: "#2563EB",
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
    fontWeight: "bold",
  },
};

export default ResultPage;