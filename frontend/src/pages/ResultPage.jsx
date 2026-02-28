import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const ResultPage = () => {
  const navigate = useNavigate();
  const { state } = useLocation();
  const [sending, setSending] = useState(false);

  if (!state) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h2>No result data found</h2>
          <button style={styles.homeBtn} onClick={() => navigate("/")}>
            Go Home
          </button>
        </div>
      </div>
    );
  }

  const {
    candidate,
    domain,
    difficulty,
    score,
    strengths = [],
    improvements = [],
    learning_plan = {},
    report,
  } = state;

  const handleDownload = () => {
    if (!report) {
      alert("Report not available");
      return;
    }

    window.open(`http://localhost:5000/reports/${report}`, "_blank");
  };

  const handleSendMail = async () => {
    if (!report) {
      alert("Report not available");
      return;
    }

    try {
      setSending(true);

      const res = await fetch("http://localhost:5000/api/send-report", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: candidate?.email,
          report: report,
        }),
      });

      if (!res.ok) throw new Error("Failed to send");

      alert("Report sent successfully ✅");
    } catch (err) {
      console.error(err);
      alert("Failed to send report");
    } finally {
      setSending(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Interview Result</h1>

        <p><b>Name:</b> {candidate?.name}</p>
        <p><b>Email:</b> {candidate?.email}</p>
        <p><b>Domain:</b> {domain}</p>
        <p><b>Difficulty:</b> {difficulty}</p>

        <h2 style={styles.score}>Score: {score}/100</h2>

        {/* Strengths */}
        <h3>✅ Strengths</h3>
        {strengths.length ? (
          <ul>
            {strengths.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        ) : (
          <p>No strengths data available.</p>
        )}

        {/* Improvements */}
        <h3>⚠ Areas to Improve</h3>
        {improvements.length ? (
          <ul>
            {improvements.map((i, idx) => (
              <li key={idx}>{i}</li>
            ))}
          </ul>
        ) : (
          <p>No improvement suggestions available.</p>
        )}

        {/* Learning Plan */}
        <h3>📘 Personalized Learning Plan</h3>

        <p>
          <b>Performance Level:</b>{" "}
          {learning_plan.performance_level || "Not Available"}
        </p>

        {learning_plan.focus_areas && (
          <>
            <h4>Focus Areas</h4>
            <ul>
              {learning_plan.focus_areas.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </>
        )}

        {learning_plan.technical_gaps && (
          <>
            <h4>Technical Gaps</h4>
            <ul>
              {learning_plan.technical_gaps.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </>
        )}

        {learning_plan.two_week_roadmap && (
          <>
            <h4>2 Week Roadmap</h4>
            <ul>
              {learning_plan.two_week_roadmap.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </>
        )}

        {learning_plan.recommended_resources && (
          <>
            <h4>Recommended Resources</h4>
            <ul>
              {learning_plan.recommended_resources.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
          </>
        )}

        {learning_plan.improvement_strategy && (
          <>
            <h4>Strategy</h4>
            <p>{learning_plan.improvement_strategy}</p>
          </>
        )}

        <div style={{ marginTop: 25 }}>
          <button style={styles.downloadBtn} onClick={handleDownload}>
            Download PDF
          </button>

          <button style={styles.mailBtn} onClick={handleSendMail}>
            {sending ? "Sending..." : "Send Report to Mail"}
          </button>

          <button style={styles.homeBtn} onClick={() => navigate("/")}>
            Go Home
          </button>
        </div>
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
    padding: 12,
    background: "#22D3EE",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
    marginRight: 10,
  },
  mailBtn: {
    padding: 12,
    background: "#10B981",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
    marginRight: 10,
  },
  homeBtn: {
    padding: 12,
    background: "#2563EB",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
  },
};

export default ResultPage;