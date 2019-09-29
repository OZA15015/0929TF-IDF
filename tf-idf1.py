import pandas as pd
#from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os
from sklearn.feature_extraction.text import CountVectorizer

# max_dfは0.5（半分以上の文書に出現する言葉はいらん）を設定
tdidf_vectorizer = CountVectorizer(input='filename', max_df=0.75)
files = ['0928_keiyou/' + path for path in os.listdir('0928_keiyou')]
# ベクトル化
X = tdidf_vectorizer.fit_transform(files).toarray()
feature_names = np.array(tdidf_vectorizer.get_feature_names())
index = X.argsort(axis=1)[:,::-1] #TF-IDF大きい順(降順)ソート, 元のインデックス取得
feature_words = [feature_names[doc] for doc in index]
i = 0
pd.set_option('display.max_rows', 400) #最大出力件数
for fwords in feature_words:
    tf_idf = [X[i][id] for id in index[i][0:400]]
    df = pd.DataFrame(tf_idf, index = fwords[:400], columns=['TF-IDF'])
    print("文書: " + files[i])
    print(df)
    print("**********************************************************")
    print("\n")
    print("\n")
    i += 1



