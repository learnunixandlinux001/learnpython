from tbselenium.tbdriver import TorBrowserDriver
from selenium.webdriver.common.action_chains import ActionChains
import pymysql.cursors
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from unidecode import unidecode
import random
from time import sleep
from datetime import datetime
from math import floor
import traceback


def insightsLogin(driver, loginusername, loginpassword):
    driver.get('http://www.udemy.com')
    sleep(random.randint(10, 15))
    # Click Login button
    loginButtonEl = driver.find_element_by_xpath("//button[text()='Log In']")
    driver.execute_script("arguments[0].click();", loginButtonEl)
    sleep(random.randint(10, 15))
    # Fill up username and password and submit
    emailTextBoxEl = driver.find_element_by_xpath("//input[@name='email']")
    emailTextBoxEl.click()
    sleep(1)
    emailTextBoxEl.send_keys(loginusername)
    sleep(random.randint(2, 5))
    passwordEl = driver.find_element_by_xpath("//input[@name='password']")
    passwordEl.click()
    sleep(1)
    passwordEl.send_keys(loginpassword)
    sleep(random.randint(2, 5))
    loginSubmitButtonEl = driver.find_element_by_xpath('//input[@name="submit"]')
    loginSubmitButtonEl.click()
    sleep(random.randint(10, 15))

f = open("db.txt","r")
hostStr = f.readline().rstrip('\n')
userStr = f.readline().rstrip('\n')
passwordStr = f.readline().rstrip('\n')
dbStr = f.readline().rstrip('\n')

instfile = open("instance.txt","r")
instanceid = instfile.readline()

connection = pymysql.connect(host=hostStr,
                             user=userStr,
                             password=passwordStr,
                             db=dbStr,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()
driver = TorBrowserDriver("/home/ubuntu/Downloads/tor-browser-linux64-8.5.4_en-US/tor-browser_en-US")
insightsLogin(driver, "onlineinstructorjohnhonai6@gmail.com", "hotmail143")

while(True):
    try:
        sql = "SELECT `term` FROM `insights` where completed is null order by rand() limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        originalTerm = result[0]['term']
        print(originalTerm)
        term = originalTerm.replace("-"," ")

        driver.implicitly_wait(10)

        driver.get("https://www.udemy.com/instructor/marketplace-insights/?q="+term+"&lang=en")
        sleep(random.randint(5, 8))

        try:
            demandEl = driver.find_element_by_xpath('//div[contains(@class,"panel-body")]/div[contains(@class,"course-label-metrics-opportunity")]/div[1]/div/div[2]')
            print(demandEl.text)
        except NoSuchElementException:
            print("trying hyphenated...")
            term = term.replace(" ","-")
            driver.get("https://www.udemy.com/instructor/marketplace-insights/?q=" + term + "&lang=en")
            sleep(random.randint(5, 8))
            demandEl = driver.find_element_by_xpath('//div[contains(@class,"panel-body")]/div[contains(@class,"course-label-metrics-opportunity")]/div[1]/div/div[2]')
            print(demandEl.text)

        demandStr = demandEl.text

        availabilityEl = driver.find_element_by_xpath('//div[contains(@class,"panel-body")]/div[contains(@class,"course-label-metrics-opportunity")]/div[2]/div/div[2]')
        print(availabilityEl.text)
        availabilityStr = availabilityEl.text

        medianEl = driver.find_element_by_xpath('//div[contains(@class,"panel-body")]/div[contains(@class,"course-label-metrics-opportunity")]/div[3]/div/div[2]')
        print(medianEl.text.lstrip('$'))
        medianStr = medianEl.text.lstrip('$')

        maxEl = driver.find_element_by_xpath('//div[contains(@class,"panel-body")]/div[contains(@class,"course-label-metrics-opportunity")]/div[4]/div/div[2]')
        print(maxEl.text.lstrip('$'))
        maxStr = maxEl.text.lstrip('$')

        percentileEl = driver.find_element_by_xpath('//div[@data-purpose="percentile"]')
        percentileStr = percentileEl.text.rstrip('st').rstrip('nd').rstrip('rd').rstrip('th')
        print(percentileStr)

        searchkeywordsEl = driver.find_element_by_xpath('//div[contains(@data-purpose,"related")]//table[contains(@class,"keyword-table")]//tbody/tr[1]/td[1]')
        print(searchkeywordsEl.text)
        searchkeywordsStr = searchkeywordsEl.text

        conversionRateEl = driver.find_element_by_xpath ('//div[@data-purpose="channels"]//div[contains(text(),"Conversion rate")]/parent::div//div[contains(@class,"mt20")]')
        print(conversionRateEl.text.rstrip('%'))
        conversionRateStr = conversionRateEl.text.rstrip('%')

        totalNumberEl = driver.find_element_by_xpath('//div[contains(@class,"panel-body")]/div[contains(@class,"course-label-metrics-supply")]/div[1]/div/div[2]')
        print(totalNumberEl.text)
        totalNumberStr = totalNumberEl.text

        highlyRatedPercentEl = driver.find_element_by_xpath('//div[contains(@class,"panel-body")]/div[contains(@class,"course-label-metrics-supply")]/div[2]/div/div[2]')
        print(highlyRatedPercentEl.text.rstrip('%'))
        highlyRatedPercentStr = highlyRatedPercentEl.text.rstrip('%')

        enrollmentsToHighlyEl = driver.find_element_by_xpath('//div[contains(@class,"panel-body")]/div[contains(@class,"course-label-metrics-supply")]/div[3]/div/div[2]')
        print(enrollmentsToHighlyEl.text.rstrip('%'))
        enrollmentsToHighlyStr = enrollmentsToHighlyEl.text.rstrip('%')

        sql = "UPDATE `insights` set demand='"+demandStr+"',courses='"+availabilityStr+"',median='"+medianStr+"',highest='"+maxStr+"',searchpercentile='"+percentileStr+"',numcourses='"+totalNumberStr+"',percenthighlyrated='"+highlyRatedPercentStr+"',enrollpercenttohighlyrated='"+enrollmentsToHighlyStr+"',conversionrate='"+conversionRateStr+"',topsearchkeywords='"+searchkeywordsStr+"',completed=now() where term='"+originalTerm+"'"
        print("Sql:" + sql)
        cursor.execute(sql)
        connection.commit()


    except Exception:
        traceback.print_exc()
        sql = "UPDATE `insights` set completed=now() where term='" + originalTerm + "'"
        print("Sql:" + sql)
        cursor.execute(sql)
        connection.commit()

