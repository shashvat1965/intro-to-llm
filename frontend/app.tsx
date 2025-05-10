import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // Import the CSS styles

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [topic, setTopic] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [questions, setQuestions] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [numberOfQuestions, setNumberOfQuestions] = useState(5);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !topic) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("topic", topic);
    formData.append("difficulty", difficulty);
    formData.append("number_of_questions", numberOfQuestions.toString());

    setLoading(true);
    try {
      const response = await axios.post(
        "http://localhost:8000/generate-questions/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setQuestions(response.data.questions);
      setTimeout(() => {
        const resultBlock = document.querySelector(".results");
        if (resultBlock) {
          resultBlock.scrollIntoView({ behavior: "smooth" });
        }
      }, 300);
    } catch (err) {
      console.error("Error generating questions:", err);
      setQuestions(["Failed to generate questions."]);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h2>Question Paper Generator</h2>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Upload PDF:
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </label>

        <label>
          Topic:
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
          />
        </label>

        <label>
          Number of Questions:
          <input
            type="number"
            value={numberOfQuestions}
            onChange={(e) => setNumberOfQuestions(Number(e.target.value))}
          />
        </label>

        <label>
          Difficulty:
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Generating..." : "Generate Questions"}
        </button>
      </form>

      {questions.length > 0 && (
        <div className="results">
          <h3>Generated Questions:</h3>
          <ol>
            {questions.map((q, i) => (
              <li key={i}>{q}</li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}

export default App;
