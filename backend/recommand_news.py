import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. CSV 데이터 로드
df = pd.read_csv("news_data.csv")

# 2. TF-IDF 벡터화 (제목 + 요약 결합)
df['content'] = df['title'] + " " + df['summary']
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['content'])

# 3. 추천 함수 정의
def recommend_news(input_title, top_n=3):
    # 입력 제목도 벡터화
    input_vec = vectorizer.transform([input_title])

    # 유사도 계산
    similarities = cosine_similarity(input_vec, tfidf_matrix).flatten()

    # 유사도 상위 N개 인덱스 추출
    top_indices = similarities.argsort()[-top_n:][::-1]

    # 결과 출력
    results = df.iloc[top_indices][['title', 'summary', 'url']]
    return results

# 4. 테스트 실행
if __name__ == "__main__":
    input_query = input("뉴스 제목을 입력하세요: ")
    recs = recommend_news(input_query)
    print("\n 추천 뉴스:")
    for i, row in recs.iterrows():
        print(f"- {row['title']} -> {row['url']}")
