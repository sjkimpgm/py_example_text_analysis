"""
다음 영화에서 영화 <알라딘>의 리뷰 및 평점 정보를 받아와서 파일로 저장
해당 리뷰 및 평점은 이후 과정에서 분석 및 예측의 test 케이스로 사용됨
"""
# 웹 크롤링에 필요한 모듈 불러오기
from urllib.request import urlopen
from bs4 import BeautifulSoup

target_movie_id = '115601'

# ===== URL만 바꾸면 다른 영화 리뷰 데이터 수집할 수 있음 ============================
# 영화 <알라딘> 리뷰 첫 번째 페이지에서 총 페이지 개수 계산하기
url = ('http://movie.daum.net/moviedb/grade?movieId=' + target_movie_id 
      + '&type=netizen&page=1')

source = BeautifulSoup(urlopen(url), 'html.parser')  # 'html5lib'
# find(name, attrs, recursive, string, **kwargs)메소드를 통해 평점 준 사람 수 추출
review = source.find('span', {'class': 'txt_menu'})

# 총 리뷰 개수를 10으로 나누어 페이지 개수를 계산할 수 있음
t = review.get_text().strip() # 평가를 한 네티즌 인원 수를 받아들여 공백을 지움
t = t[1:-1].replace(',', '')  # (2,017)에서 양쪽 괄호를 지우고 톰마를 제거해야 integer 전환시 에러가 없음
page_no = int(int(t)/10)      # 총 평점 개수를 10으로 나누고 정수로 변환해 총 페이지 개수를 계산
                              # 10으로 나누는 이유는 한 페이지당 평점이 10개씩 있어서 그렇다

# 빠른 분석을 위해서 최대 10 페이지의 리뷰만 받아옴
# if page_no > 1:
#     page_no = 1
  
review_list = []
grade_list = []
for n in range(page_no):
    # 불러오려는 url 입력하기
    url = ('http://movie.daum.net/moviedb/grade?movieId=' + target_movie_id
           + '&type=netizen&page={}'.format(n + 1))

    # urlopen() 함수로 html 파싱을 위한 BeautifulSoup 객체 생성
    source = BeautifulSoup(urlopen(url), 'html.parser')  # 'html5lib'

    # find_all(name, attrs, recursive, string, limit, **kwargs)메소드를 통해 모든 리뷰 추출
    reviews = source.find_all('p', {'class': 'desc_review'})
    grades = source.find_all('em', {'class': 'emph_grade'})

    # for 문을 통해 해당 페이지의 리뷰 추출 후 리스트에 반환
    for review in reviews:
        review_list.append(review.get_text().strip().replace('\n', ' ').replace('\t', ' ').replace('\r',' '))

    for grade in grades:
        grade_list.append(grade.get_text())

# 결과 출력하기
# for review in review_list[:10]:
#   print(review)
# 
# for grade in grade_list[:10]:
#   print(grade)
  
# 결과 txt 파일로 출력하기
file = open('movie-reviews.txt', mode='w', encoding='utf-8')
file_test = open('movie-reviews-test.txt', mode='w', encoding='utf-8')
for i in range(len(review_list)):
    file.write(grade_list[i] + "|")
    file.write(review_list[i] + '\n') # 각 리뷰를 줄 단위로 txt 파일에 저장

    # 긍정(grade >= 9)과 부정(grade <= 4) 리뷰만 따로 저장
    grade = int(grade_list[i])
    if 4 < grade < 9: continue

    # 길이가 너무 짧은 리뷰는 제외
    review = review_list[i].strip()
    if len(review) < 4: continue

    if grade <= 4:
        label = "0"
    if grade >= 9:
        label = "1"

    file_test.write(label + "|")
    file_test.write(review + '\n')
file.close()
file_test.close()

print('=' * 7, 'Job completed!!!', '=' * 30)