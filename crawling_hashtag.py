from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import random

# browser = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
browser = webdriver.Chrome()
browser.get('https://www.instagram.com/accounts/login')  
time.sleep(5)
# browser.maximize_window()   // 창 크기 최대화

## 로그인 아이디 / 비번 
USER_ID = ''
USER_PW = ''
insta_login_id = browser.find_element(by=By.NAME, value='username')
insta_login_id.click()
insta_login_id.send_keys(USER_ID)  #아이디 입력
insta_login_id.send_keys(Keys.ENTER)
time.sleep(1)
insta_login_pw = browser.find_element(by=By.NAME, value='password')
insta_login_pw.click()
insta_login_pw.send_keys(USER_PW)   # 비번입력
insta_login_pw.send_keys(Keys.ENTER)

time.sleep(5)
insta_login_record = browser.find_element(by=By.CSS_SELECTOR, value='.sqdOP.yWX7d.y3zKF     ').click() ## 로그인 정보저장 아니요
time.sleep(4)
insta_login_alarm = browser.find_element(by=By.CSS_SELECTOR, value='.aOOlW.HoLwm ').click()         ## 브라우저에서 알림 거절
time.sleep(3)
print("login success")


## 해쉬태그 크롤링할때
tag = '벚꽃'                ##크롤링할 검색어 입력
tag_search= browser.get('https://www.instagram.com/explore/tags/{}/'.format(tag))
time.sleep(10)
print("succes search_hash_tag_page")
first_img='div.v1Nh3.kIKUG._bz0w'
browser.find_element(by=By.CSS_SELECTOR, value=first_img).click()       ##첫번째 이미지 클릭
print("succes click 1st img")


# ## id의 게시물 해시태그 크롤링할때
# tag_id = "valorantesportskr"    ##찾는 사람 id 입력
# tag_id_search=browser.get("https://www.instagram.com/{}/".format(tag_id))
# time.sleep(10)
# print("succes search_{}_page".format(tag_id))
# first_img='div._9AhH0'
# browser.find_element(by=By.CSS_SELECTOR, value=first_img).click()       ##첫번째 이미지 클릭
# print("succes click 1st img")




##너무 많은 크롤링을하면 정지당하므로.. 시간을 늘리거나  가계정을 이용하거나.. 뭔가 다른방법이 필요.


hash_results = []       # 결과값을 리스트로 저장
counting = 20             ## 숫자만큼 반복
for i in range(counting):
    data = browser.find_elements(by=By.CSS_SELECTOR, value='a.xil3i') #elements 와 element의 차이점

    for j in range(len(data)):
        hash_results.append(data[j].text.replace("#","")) # 해쉬태그들 '#'을 재정의해서 제거후 저장

    
    if (i+1)%10 == 0:                           #10번째 게시물 완료시마다 print 출력
        print('{}th crawling finished!'.format(i+1))
    # WebDriverWait(browser,100).until(EC.presence_of_element_located(By.CSS_SELECTOR,'div.l8mY4.feth3 > .wpO6b '))    #TypeError: presence_of_element_located() takes 1 positional argument but 2 were given
    ## 브라우저에서 위치한 저 css_selector버튼을 찾지못하면 100초동안 대기. 
    browser.find_element(by=By.CSS_SELECTOR, value= 'div.l8mY4.feth3 > .wpO6b ').send_keys(Keys.ENTER) #다음 게시물로 이동
    time.sleep(random. uniform(3,10))  ## 3초~10초까지 랜덤하게 대기.  


df = pd.DataFrame({"hash_tags":hash_results})                           # 데이터 프레임 , 컬럼명은 "hash_tags"로 저장
df.to_csv("{}.csv".format(tag), encoding='utf-8-sig', index=False)      # csv파일로 , 저장 , 인덱스는 제외하고 저장
# df.to_csv("{}.csv".format(tag_id), encoding='utf-8-sig', index=False)   


## 이부분은 아나콘다노트북에서 켜서 그리기!

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['font.family'] ='Malgun Gothic' ##폰트설정
matplotlib.rcParams['axes.unicode_minus'] =False    ##한글폰트 사용시 마이너스 글자가 깨지는 현상을 해결

dt = pd.read_csv('E:/ts/벚꽃.csv')                  ##
x = pd.DataFrame(dt.value_counts()[:10])            ## 10번째까지 호출하고 데이터 프레임으로 변환
x.columns = ['value']                               ## 데이터프레임으로 변환한 (X)에 칼럼이름을 'value'로 지정 
x = x.reset_index(drop=False)                       ## 인덱스에 있던값을 변수로 집어넣으면서 인덱스 자리에 숫자로 전환
plt.bar(x['hash_tags'], x['value'])                 ## x축에는 'hash_tags'컬럼의 값을 , y축에는 'value' 컬럼의 숫자카운팅한 값을 이용하여 그래프 만듦
plt.xticks(rotation=70)                             ## x축 라벨 회전
plt.ylim([0, 80])                                   ## y축의 크기설정 0~80
plt.title("HASH_TAG TOP 10")                        ## 표의 제목설정





