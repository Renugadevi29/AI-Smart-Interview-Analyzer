import React, { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { generateQuestions, submitInterview } from "../services/api";

const InterviewPage = () => {
  const navigate = useNavigate();
  const { state } = useLocation();

  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answerText, setAnswerText] = useState("");
  const [answers, setAnswers] = useState([]);
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  /* 🔒 Redirect if accessed directly */
  useEffect(() => {
    if (!state) navigate("/");
  }, [state, navigate]);

  /* 🎥 WEBCAM — FINAL FIX */
  useEffect(() => {
    let activeStream;

    async function startCamera() {
      try {
        activeStream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });

        streamRef.current = activeStream;

        if (videoRef.current) {
          videoRef.current.srcObject = activeStream;
          await videoRef.current.play(); // 🔥 REQUIRED
        }
      } catch (err) {
        alert("Webcam access denied");
        console.error(err);
      }
    }

    startCamera();

    return () => {
      if (activeStream) {
        activeStream.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  /* 📥 LOAD QUESTIONS */
  useEffect(() => {
    if (!state) return;

    async function loadQuestions() {
      try {
        const res = await generateQuestions({
          domain: state.domain,
          difficulty: state.difficulty,
          count: state.count,
          language: state.language || "",
        });

        if (res?.questions?.length) {
          setQuestions(res.questions);
        } else {
          alert("No questions received");
        }
      } catch (err) {
        alert("Failed to load questions");
      } finally {
        setLoading(false);
      }
    }

    loadQuestions();
  }, [state]);

  /* 🔊 SPEAK QUESTION */
  const speakQuestion = () => {
    if (!questions[currentIndex]) return;
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(
      questions[currentIndex]
    );
    utterance.lang = "en-US";
    window.speechSynthesis.speak(utterance);
  };

  /* 🎤 SPEECH → TEXT */
  const startRecording = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition not supported");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    setListening(true);

    recognition.onresult = (e) => {
      setAnswerText(e.results[0][0].transcript);
      setListening(false);
    };

    recognition.onerror = () => setListening(false);
    recognition.start();
  };

  /* ➡️ NEXT QUESTION */
  const nextQuestion = () => {
    setAnswers((prev) => [...prev, answerText]);
    setAnswerText("");
    setCurrentIndex((prev) => prev + 1);
  };

  /* ✅ SUBMIT INTERVIEW */
  const submitInterviewHandler = async () => {
    setSubmitting(true);

    try {
      const response = await submitInterview({
        candidate: {
          name: state.name,
          email: state.email,
        },
        config: {
          domain: state.domain,
          difficulty: state.difficulty,
          language: state.language || "",
        },
        answers: [...answers, answerText],
      });

      // 🛑 STOP CAMERA
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((t) => t.stop());
      }

      navigate("/result", { state: response });
    } catch (err) {
      alert("Interview submission failed");
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  /* ⏳ STATES */
  if (loading)
    return <p style={{ color: "white", padding: 30 }}>Loading interview...</p>;

  if (!questions.length)
    return <p style={{ color: "white", padding: 30 }}>No questions available</p>;

  return (
    <div style={styles.container}>
      {/* CAMERA */}
      <div style={styles.cameraBox}>
        <video
          ref={videoRef}
          autoPlay
          muted
          playsInline
          style={styles.video}
        />
        <p style={styles.camText}>Webcam Active</p>
      </div>

      {/* INTERVIEW */}
      <div style={styles.card}>
        <h2 style={styles.title}>
          Question {currentIndex + 1} of {questions.length}
        </h2>

        <p style={styles.question}>{questions[currentIndex]}</p>

        <button style={styles.secondaryBtn} onClick={speakQuestion}>
          🔊 Hear Question
        </button>

        <button style={styles.primaryBtn} onClick={startRecording}>
          🎤 {listening ? "Listening..." : "Speak Answer"}
        </button>

        <p style={styles.answer}>
          <b>Your Answer:</b> {answerText}
        </p>

        {currentIndex < questions.length - 1 ? (
          <button style={styles.nextBtn} onClick={nextQuestion}>
            Next Question →
          </button>
        ) : (
          <button
            style={styles.submitBtn}
            onClick={submitInterviewHandler}
            disabled={submitting}
          >
            {submitting ? "Submitting..." : "Submit Interview"}
          </button>
        )}
      </div>
    </div>
  );
};

/* 🎨 STYLES */
const styles = {
  container: {
    minHeight: "100vh",
    background: "#020617",
    display: "flex",
    gap: 30,
    padding: 30,
  },
  cameraBox: {
    width: "35%",
    borderRadius: 16,
    padding: 20,
    boxShadow: "0 0 25px rgba(37,99,235,0.25)",
    textAlign: "center",
  },
  video: {
    width: "100%",
    height: "300px",
    objectFit: "cover",
    borderRadius: "12px",
    border: "2px solid #38BDF8",
    background: "#000",
  },
  camText: { marginTop: 10, color: "#38BDF8" },
  card: {
    width: "65%",
    borderRadius: 16,
    padding: 30,
    boxShadow: "0 0 30px rgba(37,99,235,0.25)",
    color: "white",
  },
  title: { color: "#38BDF8" },
  question: { fontSize: 20, margin: "20px 0" },
  primaryBtn: {
    background: "#2563EB",
    padding: 14,
    color: "#fff",
    borderRadius: 10,
    border: "none",
    cursor: "pointer",
    marginLeft: 10,
  },
  secondaryBtn: {
    background: "#0F172A",
    padding: 12,
    color: "#38BDF8",
    borderRadius: 10,
    border: "1px solid #38BDF8",
    cursor: "pointer",
  },
  answer: { marginTop: 15, color: "#CBD5E1" },
  nextBtn: {
    marginTop: 20,
    padding: 14,
    background: "#22D3EE",
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
    fontWeight: "bold",
  },
  submitBtn: {
    marginTop: 20,
    padding: 14,
    background: "#10B981",
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
    fontWeight: "bold",
  },
};

export default InterviewPage;