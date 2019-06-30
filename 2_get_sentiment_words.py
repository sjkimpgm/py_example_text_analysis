"""
NSMC(Naver Sentiment Movie Corpus) 긍정과 부정 리뷰에서 주로 나타나는 명사를 추출하여 감정 단어 사전 작성
"""

lines = open('ratings_positive.txt', mode='r', encoding='utf-8').readlines()
pos_review = []
for l in lines[:5000]:
    _, review, _ = l.split('\t', 2)
    review = review.strip()
    pos_review.append(review)

lines = open('ratings_negative.txt', mode='r', encoding='utf-8').readlines()
neg_review = []
for l in lines[:5000]:
    _, review, _ = l.split('\t', 2)
    review = review.strip()
    neg_review.append(review)

# 명사만 추출
from konlpy.tag import Okt
tx = Okt()      # Open Korean Text 형태소 분석기 변수 생성
pos_nouns = [noun for sentence in pos_review for noun in tx.nouns(sentence)] 
neg_nouns = [noun for sentence in neg_review for noun in tx.nouns(sentence)] 

# Counter를 이용하여 자주 사용되는 단어 추출
from collections import Counter
pos_counter = Counter(pos_nouns)
neg_counter = Counter(neg_nouns)

pos_common = pos_counter.most_common(100)
neg_common = neg_counter.most_common(100)

pos_common_noun = set([pair[0] for pair in pos_common])
neg_common_noun = set([pair[0] for pair in neg_common])

# 긍정과 부정에서 겹치는 단어 삭제
pos_only_noun = pos_common_noun - neg_common_noun
neg_only_noun = neg_common_noun - pos_common_noun

pos_sentiment = []
for p in pos_common:
    if p[0] in pos_only_noun:
        pos_sentiment.append(p[0])

neg_sentiment = []
for p in neg_common:
    if p[0] in neg_only_noun:
        neg_sentiment.append(p[0])

# 결과 txt 파일로 출력하기
print(pos_sentiment[:10])
print(neg_sentiment[:10])

file = open('sentiment-words.txt', mode='w', encoding='utf-8')
file.write("|".join(pos_sentiment) + '\n')
file.write("|".join(neg_sentiment) + '\n')
file.close()

print('=' * 7, 'Job completed!!!', '=' * 30)