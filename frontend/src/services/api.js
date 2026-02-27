const BASE_URL = "http://localhost:5000";

/* =========================================
   1️⃣ Generate Interview Questions
========================================= */
export async function generateQuestions(payload) {
  try {
    const res = await fetch(`${BASE_URL}/api/generate-questions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      throw new Error("Failed to generate questions");
    }

    return await res.json();
  } catch (error) {
    console.error("Generate Questions Error:", error);
    return { questions: [] };
  }
}

/* =========================================
   2️⃣ Submit Interview & Get Result
========================================= */
export const submitInterview = async (payload) => {
  const res = await fetch("http://localhost:5000/api/interview/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Interview submission failed");
  }

  return await res.json(); // 🔥 THIS IS CRITICAL
};

export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append("resume", file);

  const res = await fetch("http://localhost:5000/api/resume/upload", {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Resume upload failed");
  }

  return await res.json();
};