### 네이버 데이터랩 실시간 긁어와서 sorting 해주는 코드 
 
import pandas as pd
from tqdm import tqdm
import time
import os
from selenium import webdriver
import numpy as np
import datetime
 
now = datetime.datetime.now()
yesterday = now - datetime.timedelta(1)
 
now_year = str(now.year)
yes_year = str(yesterday.year)
 
now_month = str(now.month).zfill(2)
yes_month = str(yesterday.month).zfill(2)
 
now_day = str(now.day).zfill(2)
yes_day = str(yesterday.day).zfill(2)
 
os.chdir("/Users/janggukjin/Desktop")
# os.getcwd()
file = '네이버_데이터랩_실시간키워드_' + now_year + now_month + now_day + '.xlsx'
 
keyword_list = pd.read_excel("네이버_데이터랩_실시간키워드_181014.xlsx")
result_word_yes = []
result_word_tod = []
result_cnt_yes = []
result_cnt_tod = []
result_url_yes = []
result_url_tod = []
 
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome('/Users/mycelebs/Desktop/chromedriver', chrome_options=chrome_options)
 
for i in tqdm(range(12,24)):
    try:
        number = str(i).zfill(2)
        url = 'https://datalab.naver.com/keyword/realtimeList.naver?datetime=' + yes_year + '-' + yes_month + '-' + yes_day+ 'T' + number + '%3A00%3A00'
        driver.get(url)
        for j in range(len(keyword_list)):
            data = driver.find_element_by_xpath(
                '//*[@id="content"]/div/div[3]/div/div/div[1]/div/div/ul/li[' + str(j + 1) + ']').text
            column = str(i) + "시"
            column2 = '비고(' + str(i) + ':00)'
            keyword_list[column].iloc[j] = data
            keyword_list[column2].iloc[j] = np.nan
            data2 = data.partition(' ')[2]
            result_word_yes.append(data2)
 
    except Exception as e:
        print(e)
 
 
for i in tqdm(range(0, 12)):
    try:
        number = str(i).zfill(2)
        url = 'https://datalab.naver.com/keyword/realtimeList.naver?datetime=' + now_year + '-' + now_month + '-' + now_day + 'T' + number + '%3A00%3A00'
        driver.get(url)
        for j in range(len(keyword_list)):
            data = driver.find_element_by_xpath('//*[@id="content"]/div/div[3]/div/div/div[1]/div/div/ul/li[' + str(j + 1) + ']').text
            column = str(i) + "시"
            column2 = '비고(' + str(i) + ':00)'
            keyword_list[column].iloc[j] = data
            keyword_list[column2].iloc[j] = np.nan
            data2 = data.split(' ')[1]
            result_word_tod.append(data2)
 
    except Exception as e:
        print(e)
 
for j in tqdm(range(len(result_word_yes))):
    yes_r_count = result_word_yes.count(result_word_yes[j])
    tod_r_count = result_word_tod.count(result_word_tod[j])
    yes_r_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=' + result_word_yes[j]
    tod_r_url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=' + result_word_tod[j]
    result_cnt_yes.append(yes_r_count)
    result_cnt_tod.append(tod_r_count)
    result_url_yes.append(yes_r_url)
    result_url_tod.append(tod_r_url)
 
 
yes_data_frame = {'전일(12시~23시)' : result_word_yes,'전일 검색어 count' : result_cnt_yes ,'전일 news_url' : result_url_yes}
tod_data_frame = {'금일(0시~11시)' : result_word_tod,'금일 검색어 count' : result_cnt_tod, '금일 news_url' : result_url_tod}
 
yes_df = pd.DataFrame(yes_data_frame, columns=['전일(12시~23시)','전일 검색어 count', '전일 news_url'])
tod_df = pd.DataFrame(tod_data_frame, columns=['금일(0시~11시)','금일 검색어 count', '금일 news_url'])
 
df_yesterday = yes_df.drop_duplicates()
df_today = tod_df.drop_duplicates()
 
df_yesterday = df_yesterday.sort_values(['전일 검색어 count'],ascending = [False])
df_today = df_today.sort_values(['금일 검색어 count'],ascending = [False])
 
df_yesterday = df_yesterday.reset_index(drop = True)
df_today = df_today.reset_index(drop = True)
 
writer = pd.ExcelWriter(os.getcwd() + '/' + file , engine = 'xlsxwriter')
#keyword_list = keyword_list.set_index('16시')
keyword_list.to_excel(writer, '실검', index = False)
df_yesterday.to_excel(writer, '전일 결과')
df_today.to_excel(writer, '금일 결과')
 
writer.save()
writer.close()
driver.close()