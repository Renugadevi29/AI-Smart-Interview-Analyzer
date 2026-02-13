import React, { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { generateQuestions, submitInterview } from "../services/api";

const InterviewPage = () => {
  const navigate = useNavigate();
  const { state } = useLocation(); // ✅ ONLY use state

  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const recognitionRef = useRef(null);

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answerText, setAnswerText] = useState("");
  const [answers, setAnswers] = useState([]);
  const [listening, setListening] = useState(false);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  /* ============================
      🔒 REDIRECT IF NO STATE
  ============================ */
  useEffect(() => {
    if (!state) {
      alert("Session expired. Please start again.");
      navigate("/");
    }
  }, [state, navigate]);

  /* ============================
      🎥 CAMERA
  ============================ */
  useEffect(() => {
    if (!state) return;

    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });

        streamRef.current = stream;

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error(err);
        alert("Camera access denied");
      }
    };

    startCamera();

    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, [state]);

  /* ============================
      🎤 SPEECH
  ============================ */
  useEffect(() => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event) => {
      setAnswerText(event.results[0][0].transcript);
      setListening(false);
    };

    recognition.onend = () => setListening(false);
    recognition.onerror = () => setListening(false);

    recognitionRef.current = recognition;
  }, []);

  /* ============================
      📥 LOAD QUESTIONS
  ============================ */
  useEffect(() => {
    if (!state) return;

    const loadQuestions = async () => {
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
          alert("No questions received from backend");
        }
      } catch (err) {
        console.error(err);
        alert("Failed to load questions");
      } finally {
        setLoading(false);
      }
    };

    loadQuestions();
  }, [state]);

  /* ============================
      🔊 SPEAK QUESTION
  ============================ */
  const speakQuestion = () => {
    if (!questions[currentIndex]) return;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(
      questions[currentIndex]
    );
    utterance.lang = "en-US";
    window.speechSynthesis.speak(utterance);
  };

  /* ============================
      🎤 RECORD
  ============================ */
  const startRecording = () => {
    if (!recognitionRef.current || listening) return;

    setAnswerText("");
    setListening(true);

    try {
      recognitionRef.current.start();
    } catch (err) {
      console.warn("Already started");
    }
  };

  /* ============================
      ➡️ NEXT
  ============================ */
  const nextQuestion = () => {
    if (!answerText.trim()) {
      alert("Please answer before continuing");
      return;
    }

    setAnswers((prev) => [...prev, answerText.trim()]);
    setAnswerText("");
    setCurrentIndex((prev) => prev + 1);
  };

  /* ============================
      ✅ SUBMIT
  ============================ */
  const submitInterviewHandler = async () => {
    if (!answerText.trim()) {
      alert("Last answer missing");
      return;
    }

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
        answers: [...answers, answerText.trim()],
      });

      navigate("/result", { state: response });
    } catch (err) {
      console.error(err);
      alert("Interview submission failed");
    } finally {
      setSubmitting(false);
    }
  };

  /* ============================
      UI
  ============================ */

  if (loading)
    return <p style={{ color: "white", padding: 30 }}>Loading...</p>;

  if (!questions.length)
    return <p style={{ color: "white", padding: 30 }}>No questions</p>;

  return (
    <div style={styles.container}>
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

      <div style={styles.card}>
        <h2 style={styles.title}>
          Question {currentIndex + 1} / {questions.length}
        </h2>

        <p style={styles.question}>
          {questions[currentIndex]}
        </p>

        <button style={styles.secondaryBtn} onClick={speakQuestion}>
          🔊 Hear Question
        </button>

        <button
          style={styles.primaryBtn}
          onClick={startRecording}
          disabled={listening}
        >
          🎤 {listening ? "Listening..." : "Speak"}
        </button>

        <p style={styles.answer}>
          <b>Your Answer:</b> {answerText}
        </p>

        {currentIndex < questions.length - 1 ? (
          <button style={styles.nextBtn} onClick={nextQuestion}>
            Next →
          </button>
        ) : (
          <button
            style={styles.submitBtn}
            onClick={submitInterviewHandler}
            disabled={submitting}
          >
            {submitting ? "Submitting..." : "Submit"}
          </button>
        )}
      </div>
    </div>
  );
};

/* STYLES */
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
    padding: 20,
    textAlign: "center",
  },
  video: {
    width: "100%",
    height: 300,
    objectFit: "cover",
    borderRadius: 12,
    border: "2px solid #38BDF8",
    background: "#000",
  },
  camText: { marginTop: 10, color: "#38BDF8" },
  card: {
    width: "65%",
    padding: 30,
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
    marginLeft: 10,
  },
  secondaryBtn: {
    background: "#0F172A",
    padding: 12,
    color: "#38BDF8",
    border: "1px solid #38BDF8",
    borderRadius: 10,
  },
  answer: { marginTop: 15, color: "#CBD5E1" },
  nextBtn: {
    marginTop: 20,
    padding: 14,
    background: "#22D3EE",
    borderRadius: 10,
    border: "none",
  },
  submitBtn: {
    marginTop: 20,
    padding: 14,
    background: "#10B981",
    borderRadius: 10,
    border: "none",
  },
};

export default InterviewPage;