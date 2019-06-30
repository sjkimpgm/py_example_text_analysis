"""
TF-IDF 기법을 활용하여 리뷰를 벡터(vector)화 한다.
이를 기본적인 기계 학습 기법인 나이브 베이즈 분류기와 서포트 벡터 머신으로 학습한다.
학습된 분류기를 통해 리뷰의 긍정 부정을 예측하고 그 정확도를 확인한다.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
from konlpy.tag import Okt

tx = Okt()      # Open Korean Text 형태소 분석기 변수 생성

# 학습 데이터 및 라벨 준비
train_data = []
train_label = []
for file_path in ['ratings_positive.txt', 'ratings_negative.txt']:
    lines = open(file_path, mode='r', encoding='utf-8').readlines()
    for sentence in lines[:5000]:
        _, review, label = sentence.split('\t', 2)
        
        pos = ['/'.join(t) for t in tx.pos(review, norm=True, stem=True)]
        pos = ' '.join(pos)
        train_data.append(pos)
        train_label.append(int(label))

vectorizer = TfidfVectorizer(min_df=2,sublinear_tf=True)
train_tfidf = vectorizer.fit_transform(train_data)

# 테스트 데이터 및 라벨 준비
test_data = []
test_label = []
lines = open("movie-reviews-test.txt", mode='r', encoding='utf-8').readlines()
for sentence in lines:
    label, review = sentence.split('|', 1)
    
    pos = ['/'.join(t) for t in tx.pos(review, norm=True, stem=True)]
    pos = ' '.join(pos)
    test_data.append(pos)
    test_label.append(int(label))

test_tfidf = vectorizer.transform(test_data)

# NB classifier
Naive = naive_bayes.MultinomialNB()
Naive.fit(train_tfidf, train_label)

predictions_NB = Naive.predict(test_tfidf)
print("나이브 베이즈 정확도 -> {:3.2f} %".format(accuracy_score(predictions_NB, test_label)*100))

# Classifier - Algorithm - SVM
SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto')
SVM.fit(train_tfidf,train_label)

predictions_SVM = SVM.predict(test_tfidf)
print("SVM 정확도 -> {:3.2f} %".format(accuracy_score(predictions_SVM, test_label)*100))

print('=' * 7, 'Job completed!!!', '=' * 30)