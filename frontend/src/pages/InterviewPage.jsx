import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { generateQuestions, submitInterview } from "../services/api";
import CameraRecorder from "../components/CameraRecorder";

const InterviewPage = () => {
  const navigate = useNavigate();
  const { state } = useLocation();

  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answerText, setAnswerText] = useState("");
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [listening, setListening] = useState(false);

  useEffect(() => {
    if (!state) navigate("/");
  }, [state, navigate]);

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
          setQuestions(res.questions.slice(0, state.count));
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    loadQuestions();
  }, [state]);

  /* 🔊 TEXT TO SPEECH */
  const speakQuestion = () => {
  if (!questions[currentIndex]) return;

  const text = questions[currentIndex];

  const synth = window.speechSynthesis;

  const speak = () => {
    if (synth.speaking) {
      synth.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "en-US";
    utterance.rate = 1;
    utterance.pitch = 1;

    // Select a proper English voice
    const voices = synth.getVoices();
    const englishVoice = voices.find(v => v.lang === "en-US");

    if (englishVoice) {
      utterance.voice = englishVoice;
    }

    synth.speak(utterance);
  };

  // If voices not loaded yet
  if (synth.getVoices().length === 0) {
    synth.onvoiceschanged = () => {
      speak();
    };
  } else {
    speak();
  }
};
  /* 🎤 SPEECH TO TEXT */
  const startRecording = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech recognition not supported in this browser");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    setListening(true);

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setAnswerText(transcript);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error:", event.error);
      alert("Microphone error: " + event.error);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
  };

  const nextQuestion = () => {
    if (!answerText.trim()) {
      alert("Please answer before continuing.");
      return;
    }

    setAnswers((prev) => [...prev, answerText.trim()]);
    setAnswerText("");
    setCurrentIndex((prev) => prev + 1);
  };

  const submitInterviewHandler = async () => {
    if (!answerText.trim()) {
      alert("Please answer the last question.");
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
        questions: questions,
      });

      navigate("/result", { state: response });
    } catch (err) {
      console.error(err);
      alert("Interview submission failed");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading)
    return <p style={{ color: "white", padding: 30 }}>Loading...</p>;

  if (!questions.length)
    return <p style={{ color: "white", padding: 30 }}>No questions available</p>;

  return (
    <div style={styles.container}>
      <div style={styles.cameraBox}>
        <CameraRecorder />
      </div>

      <div style={styles.card}>
        <h2>
          Question {currentIndex + 1} of {questions.length}
        </h2>

        <p style={styles.question}>{questions[currentIndex]}</p>

        <div style={{ marginBottom: 15 }}>
          <button style={styles.secondaryBtn} onClick={speakQuestion}>
            🔊 Hear Question
          </button>

          <button style={styles.primaryBtn} onClick={startRecording}>
            🎤 {listening ? "Listening..." : "Speak Answer"}
          </button>
        </div>

        <textarea
          value={answerText}
          onChange={(e) => setAnswerText(e.target.value)}
          placeholder="You can speak or type your answer..."
          style={styles.textarea}
        />

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
  },
  card: {
    width: "65%",
    color: "white",
  },
  question: {
    fontSize: 20,
    margin: "20px 0",
  },
  primaryBtn: {
    background: "#2563EB",
    padding: 12,
    color: "#fff",
    borderRadius: 8,
    border: "none",
    marginLeft: 10,
    cursor: "pointer",
  },
  secondaryBtn: {
    background: "#0F172A",
    padding: 12,
    color: "#38BDF8",
    border: "1px solid #38BDF8",
    borderRadius: 8,
    cursor: "pointer",
  },
  textarea: {
    width: "100%",
    minHeight: 120,
    padding: 12,
    borderRadius: 8,
    border: "1px solid #334155",
    background: "#0F172A",
    color: "white",
    marginBottom: 20,
  },
  nextBtn: {
    padding: 12,
    background: "#22D3EE",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
  },
  submitBtn: {
    padding: 12,
    background: "#10B981",
    borderRadius: 8,
    border: "none",
    cursor: "pointer",
  },
};

export default InterviewPage;