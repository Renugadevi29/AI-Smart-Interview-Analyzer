import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const InterviewSetupPage = () => {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [domain, setDomain] = useState("");
  const [language, setLanguage] = useState("");
  const [difficulty, setDifficulty] = useState("easy");
  const [count, setCount] = useState(3);

  const startInterview = () => {
    if (!name.trim() || !email.trim() || !domain) {
      alert("Please fill all required fields");
      return;
    }

    if (domain === "Technical" && !language.trim()) {
      alert("Please enter a technology");
      return;
    }

    const config = {
      name: name.trim(),
      email: email.trim(),
      domain,
      difficulty,
      count,
      language: domain === "Technical" ? language.trim() : "",
    };

    // ✅ Save to sessionStorage
    sessionStorage.setItem("interviewConfig", JSON.stringify(config));

    navigate("/interview");
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h2 style={styles.title}>Interview Setup</h2>

        <input
          style={styles.input}
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          style={styles.input}
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <select
          style={styles.input}
          value={domain}
          onChange={(e) => {
            setDomain(e.target.value);
            setLanguage("");
          }}
        >
          <option value="">Select Domain</option>
          <option value="Technical">Technical</option>
          <option value="HR">HR</option>
          <option value="Behavioral">Behavioral</option>
        </select>

        {domain === "Technical" && (
          <input
            style={styles.input}
            placeholder="Technology (Python, Java, SQL...)"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          />
        )}

        <select
          style={styles.input}
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>

        <select
          style={styles.input}
          value={count}
          onChange={(e) => setCount(Number(e.target.value))}
        >
          <option value={3}>3 Questions</option>
          <option value={5}>5 Questions</option>
          <option value={10}>10 Questions</option>
        </select>

        <button style={styles.button} onClick={startInterview}>
          Start Interview
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
  },
  card: {
    padding: 40,
    borderRadius: 16,
    width: 420,
    background: "#020617",
    boxShadow: "0 0 30px rgba(37,99,235,0.25)",
  },
  title: {
    color: "#38BDF8",
    textAlign: "center",
    marginBottom: 25,
  },
  input: {
    width: "100%",
    padding: 12,
    marginBottom: 15,
    borderRadius: 8,
    border: "none",
    background: "#0F172A",
    color: "#E5E7EB",
  },
  button: {
    width: "100%",
    padding: 14,
    borderRadius: 10,
    border: "none",
    background: "#2563EB",
    color: "#fff",
    fontWeight: "bold",
    cursor: "pointer",
  },
};

export default InterviewSetupPage;
