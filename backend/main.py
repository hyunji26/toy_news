from fastapi.responses import JSONResponse
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import recommand_news
from fastapi import FastAPI,Query
from fastapi.middleware.cors import CORSMiddleware

# 1. 앱 초기화
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 2. 데이터 로드 & 벡터화
df = pd.read_csv("news_data.csv")
df['content'] = df['title'] + " " + df['summary']

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['content'])

def recommend_news(input_title, top_n=3):
    if not input_title.strip():
        return pd.DataFrame([{
            "title": "입력된 제목이 비어 있거나 유효하지 않습니다",
            "summary": "다시 입력해주세요.",
            "url": "#"
        }])

    input_vec = vectorizer.transform([input_title])

    if input_vec.nnz == 0:
        print(f"[로그] 입력 '{input_title}' → 희소 벡터. 관련 뉴스 없음.")
        return pd.DataFrame([{
            "title": "관련 뉴스가 없습니다",
            "summary": "입력하신 키워드와 유사한 뉴스가 존재하지 않아요.",
            "url": "#"
        }])

    similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()

    print(f"\n[ 유사도 로그] 입력: '{input_title}'")
    scored_news = []
    for i, sim in enumerate(similarities):
        print(f"- {df.iloc[i]['title']}: {sim:.4f}")
        if sim > 0:
            scored_news.append((i, sim))

    if not scored_news:
        return pd.DataFrame([{
            "title": "관련 뉴스가 없습니다",
            "summary": "유사도가 0인 뉴스는 제외되었어요.",
            "url": "#"
        }])

    # 유사도 순으로 정렬한 뒤 전부 반환
    sorted_indices = sorted(scored_news, key=lambda x: x[1], reverse=True)
    selected_indices = [i for i, _ in sorted_indices]

    print("[ 추천 결과]", df.iloc[selected_indices]['title'].tolist())

    return df.iloc[selected_indices][['title', 'summary', 'url']]




# 4. API 라우터
@app.get("/recommend")
def get_recommendation(title: str = Query(..., description="뉴스 제목")):
    try:
        results = recommend_news(title)
        return JSONResponse(content=results.to_dict(orient="records"))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
