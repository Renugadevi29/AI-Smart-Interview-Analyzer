import React from "react";
import { useNavigate } from "react-router-dom";

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>AI Smart Interview Analyzer</h1>
        <p style={styles.subtitle}>
          Practice real-time AI-powered mock interviews with voice, webcam, and personalized learning plans.
        </p>

        <button style={styles.button} onClick={() => navigate("/setup")}>
          Start Mock Interview
        </button>

        <p style={styles.note}>No signup required • Instant feedback</p>
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
  },
  card: {
    background: "#020617",
    padding: 50,
    borderRadius: 20,
    width: 520,
    textAlign: "center",
    boxShadow: "0 0 40px rgba(37,99,235,0.3)",
  },
  title: { color: "#38BDF8", fontSize: 32 },
  subtitle: { color: "#CBD5E1", marginTop: 15 },
  button: {
    marginTop: 30,
    padding: 16,
    width: "100%",
    borderRadius: 12,
    border: "none",
    background: "#2563EB",
    color: "#fff",
    fontSize: 18,
    cursor: "pointer",
    fontWeight: "bold",
  },
  note: { marginTop: 15, color: "#94A3B8" },
};

export default LandingPage;
