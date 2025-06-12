import React, { useState } from "react";
import axios from "axios";

function App() {
  const [inputTitle, setInputTitle] = useState("");
  const [results, setResults] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    
    try {
      const res = await axios.get("http://localhost:8081/recommend", {
        params: { title: inputTitle },
      });
      setResults(res.data);
    } catch (err) {
      alert("추천 결과를 가져오는 데 실패했어요.");
      console.error(err);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>📰 뉴스 추천 시스템</h1>
      <p style={styles.subtitle}>관심 있는 뉴스 제목을 입력하면 관련 뉴스를 추천해드려요</p>
      
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          value={inputTitle}
          onChange={(e) => setInputTitle(e.target.value)}
          placeholder="예: 아이폰15 출시"
          style={styles.input}
        />
        <button type="submit" style={styles.button}>
          🔍 추천받기
        </button>
      </form>

      <div style={styles.results}>
        {results.length > 0 && <h2 style={styles.resultTitle}>📌 추천된 뉴스</h2>}
        {results.map((news, idx) => (
          <div key={idx} style={styles.card}>
            <a href={news.url} target="_blank" rel="noreferrer" style={styles.link}>
              <h3 style={styles.newsTitle}>{news.title}</h3>
            </a>
            <p style={styles.summary}>{news.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "720px",
    margin: "60px auto",
    padding: "20px",
    fontFamily: "'Segoe UI', sans-serif",
    backgroundColor: "#fdfdfd",
  },
  title: {
    fontSize: "2.4rem",
    textAlign: "center",
    marginBottom: "10px",
    color: "#2c3e50",
  },
  subtitle: {
    fontSize: "1rem",
    textAlign: "center",
    color: "#555",
    marginBottom: "30px",
  },
  form: {
    display: "flex",
    gap: "10px",
    marginBottom: "40px",
  },
  input: {
    flex: 1,
    padding: "12px 16px",
    fontSize: "16px",
    borderRadius: "6px",
    border: "1px solid #ccc",
  },
  button: {
    padding: "12px 20px",
    backgroundColor: "#1abc9c",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontWeight: "bold",
    transition: "0.2s",
  },
  results: {
    display: "flex",
    flexDirection: "column",
    gap: "20px",
  },
  resultTitle: {
    fontSize: "1.6rem",
    borderBottom: "1px solid #ddd",
    paddingBottom: "10px",
    marginBottom: "20px",
    color: "#34495e",
  },
  card: {
    padding: "20px",
    border: "1px solid #eee",
    borderRadius: "10px",
    backgroundColor: "#fff",
    boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
  },
  link: {
    textDecoration: "none",
    color: "#2c3e50",
  },
  newsTitle: {
    fontSize: "18px",
    marginBottom: "6px",
  },
  summary: {
    fontSize: "15px",
    color: "#666",
  },
};

export default App;
