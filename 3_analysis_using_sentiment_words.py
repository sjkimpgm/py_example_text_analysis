"""
긍정 부정 단어를 통해서 리뷰의 긍정 부정을 예측하다.
이를 실제 평점과 비교하여 정확도를 확인한다.
"""

file_sentiment = open('sentiment-words.txt', mode='r', encoding='utf-8').readlines()
pos_sentiment = file_sentiment[0].strip().split("|")
strong_pos_sentiment = pos_sentiment[:10]
pos_sentiment = pos_sentiment[10:]

neg_sentiment = file_sentiment[1].strip().split("|")
strong_neg_sentiment = neg_sentiment[:10]
neg_sentiment = neg_sentiment[10:]

from konlpy.tag import Okt
tx = Okt()      # Open Korean Text 형태소 분석기 변수 생성

count_correct = 0
count_ambiguous = 0
lines = open('movie-reviews-test.txt', mode='r', encoding='utf-8').readlines()
for l in lines:
    label, review = l.split('|', 1)

    polarity = 0
    for noun in tx.nouns(review):
        if noun in strong_pos_sentiment:
            polarity += 2
        elif noun in pos_sentiment:
            polarity += 1
        elif noun in strong_neg_sentiment:
            polarity -= 2
        elif noun in neg_sentiment:
            polarity -= 1
        
    if polarity > 0:
        prediction = "1"
    elif polarity < 0:
        prediction = "0"
    else:
        count_ambiguous += 1
        continue

    if label == prediction:
        result = "성공"
        count_correct += 1

print("정확도 = {:3.2f} % = {} / {}".format(count_correct/len(lines) * 100, count_correct, len(lines)))
print("정확도(w/o ambiguous) = {:3.2f} % = {} / {}".format(count_correct/(len(lines)-count_ambiguous) * 100, count_correct, len(lines)-count_ambiguous))

print('=' * 7, 'Job completed!!!', '=' * 30)