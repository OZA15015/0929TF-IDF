import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# ベクトル化する文字列
sample = np.array(['Apple computer of the apple mark', 'linux computer', 'windows computer'])

# TfidfVectorizer
vec_tfidf = TfidfVectorizer()
# ベクトル化
X = vec_tfidf.fit_transform(sample).toarray()
feature_names = np.array(vec_tfidf.get_feature_names())
index = X.argsort(axis=1)[:,::-1] #TF-IDF大きい順(降順)ソート, 元のインデックス取得
feature_words = [feature_names[doc] for doc in index]
i = 0
for fwords in feature_words:
    tf_idf = [X[i][id] for id in index[i]]
    df = pd.DataFrame(tf_idf, index = fwords[:7], columns=['TF-IDF'])
    print("文書: " + sample[i])
    print(df)
    print("**********************************************************")
    print("\n")
    print("\n")
    i += 1



