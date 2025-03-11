from selenium import webdriver
from selenium.webdriver.common.by import By
import json, time  
from webdriver_manager.chrome import ChromeDriverManager
from connectToDB import connectToPostgreSQL

# Bu 


def get_video_results():
    con,cur = connectToPostgreSQL()

    driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(f'https://www.youtube.com/results?search_query= fenerbahçe galatasaray')
    youtube_data = []

    while True:
        end_result = driver.find_element(By.CSS_SELECTOR,'#message').is_displayed()
        driver.execute_script("var scrollingElement = (document.scrollingElement || document.body);scrollingElement.scrollTop = scrollingElement.scrollHeight;")
        time.sleep(1)

        if end_result == True:
            break

    print('Extracting results. It might take a while...\n\n')

    for result in driver.find_elements(By.CSS_SELECTOR,".text-wrapper.style-scope.ytd-video-renderer"):
        # print("*******RESULT********",result)
        
        title = result.find_element(By.CSS_SELECTOR,'.title-and-badge.style-scope.ytd-video-renderer').text
        videoURL = result.find_element(By.CSS_SELECTOR,'.title-and-badge.style-scope.ytd-video-renderer a').get_attribute('href')
        channelName = result.find_element(By.CSS_SELECTOR,'.long-byline').text
        channelURL = result.find_element(By.CSS_SELECTOR,'#text > a').get_attribute('href')
        view = result.find_element(By.CSS_SELECTOR,'.style-scope ytd-video-meta-block').text.split('\n')[0]
        # print("View",view,type(view))

        statement ="INSERT INTO youtube.ytdownloadvideourl(videoURL,title,view,channelName,channelURL) VALUES (%s,%s,%s,%s,%s)"
        cur.execute(statement,(str(videoURL),str(title),str(view),str(channelName),str(channelURL),))
        con.commit()
    print("\nCommited the table")
    con.close()
    print("Closed the table\n")

    
get_video_results()
