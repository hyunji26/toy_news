from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


corpus = [
    "소년과 로봇의 우정 이야기",
    "로봇이 세상을 구한다",
    "고양이와 소년이 여행을 떠난다",
    "강아지와 소녀의 감동 스토리",
    "로봇이 인간을 도와주는 미래 사회"
]

# 2. TF-IDF 벡터화
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

# 3. cosine similarity 계산 (5x5 유사도 행렬)
cos_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# 4. 유사도 DataFrame으로 보기 좋게 출력
df = pd.DataFrame(cos_sim, columns=range(len(corpus)), index=range(len(corpus)))
print(df.round(2))
