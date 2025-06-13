from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

# 앱 초기화
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 데이터 로드 및 전처리
df = pd.read_csv("news_data.csv")
df['content'] = df['title'] + " " + df['summary'].str.lower()

# BERT 기반 임베딩 모델 로드
model = SentenceTransformer("jhgan/ko-sbert-nli")
corpus_embeddings = model.encode(df['content'].tolist(), convert_to_tensor=True)

# 뉴스 추천 함수
def recommend_news(input_title: str):
    if not input_title.strip():
        return pd.DataFrame([{
            "title": "입력된 제목이 비어 있거나 유효하지 않습니다",
            "summary": "다시 입력해주세요.",
            "url": "#"
        }])

    # 입력 문장 임베딩
    input_embedding = model.encode([input_title], convert_to_tensor=True)
    cosine_scores = util.cos_sim(input_embedding, corpus_embeddings)[0]

    print(f"\n[ 유사도 로그] 입력: '{input_title}'")
    scored_news = []
    for i, sim in enumerate(cosine_scores):
        print(f"- {df.iloc[i]['title']}: {sim:.4f}")
        if sim.item() > 0.251:  # 유사도 필터링 기준
            scored_news.append((i, sim.item()))

    if not scored_news:
        return pd.DataFrame([{
            "title": "관련 뉴스가 없습니다",
            "summary": "입력하신 키워드와 관련된 뉴스가 충분하지 않아요.",
            "url": "#"
        }])

    # 유사도 내림차순 정렬 후 상위 5개 추출
    sorted_indices = sorted(scored_news, key=lambda x: x[1], reverse=True)
    top_indices = [i for i, _ in sorted_indices[:5]]  # 상위 5개만

    print("[ 추천 결과]", df.iloc[top_indices]['title'].tolist())
    return df.iloc[top_indices][['title', 'summary', 'url']]


# API 라우터
@app.get("/recommend")
def get_recommendation(title: str = Query(..., description="뉴스 제목")):
    try:
        results = recommend_news(title)
        return JSONResponse(content=results.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
