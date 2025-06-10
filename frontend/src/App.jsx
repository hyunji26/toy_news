// 1️⃣ App.jsx
import React, { useState } from "react";
import axios from "axios";

function App() {
  const [inputTitle, setInputTitle] = useState("");
  const [results, setResults] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.get(`http://localhost:8001/recommend`, {
        params: { title: inputTitle },
      });
      setResults(res.data);
    } catch (err) {
      alert("추천 결과를 가져오는 데 실패했어요.");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>📰 뉴스 제목 기반 추천</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={inputTitle}
          onChange={(e) => setInputTitle(e.target.value)}
          placeholder="뉴스 제목을 입력하세요"
          style={{ width: "100%", padding: 10, fontSize: 16 }}
        />
        <button type="submit" style={{ marginTop: 10, padding: 10, width: "100%" }}>
          추천받기
        </button>
      </form>

      <div style={{ marginTop: 30 }}>
        {results.length > 0 && <h3>🔍 추천 뉴스</h3>}
        {results.map((news, idx) => (
          <div key={idx} style={{ marginBottom: 20 }}>
            <a href={news.url} target="_blank" rel="noreferrer">
              <h4 style={{ margin: 0 }}>{news.title}</h4>
            </a>
            <p style={{ margin: 0, color: "gray" }}>{news.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
