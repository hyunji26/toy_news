from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import recommand_news

# 1. 앱 초기화
app = FastAPI()

# 2. 데이터 로드 & 벡터화
df = pd.read_csv("news_data.csv")
df['content'] = df['title'] + " " + df['summary']

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['content'])

# 3. 추천 함수
def recommend_news(input_title, top_n=3):
    input_vec = vectorizer.transform([input_title])
    similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]
    return df.iloc[top_indices][['title', 'summary', 'url']]

# 4. API 라우터
@app.get("/recommend")
def get_recommendation(title: str = Query(..., description="뉴스 제목")):
    try:
        results = recommend_news(title)
        return JSONResponse(content=results.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
