from tbselenium.tbdriver import TorBrowserDriver
from selenium.webdriver.common.action_chains import ActionChains
import pymysql.cursors
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from unidecode import unidecode
import random
from time import sleep
from datetime import datetime
import traceback

searchKeywords = ["java", "java programming", "linux", "unix", "python", "python programming", "java", "web",
                  "internet", "blockchain", "javascript", "video", "animation", "hacking", "python coding", "coding",
                  "database", "sql", "angular", "operating system", "networking", "networks", "architecture",
                  "software", "learning", "security", "server", "nodejs", "react", "html", "css", "html5", "ios ",
                  "android apps", "data science", "cloud", "aws", "developer", "bitcoin", "html coding",
                  "python coding", "android coding", "mobile app", "selenium", "testing", "html css", "framework",
                  "spring", "artificial", "command line", "advanced", "rest api", "cisco", "certification"]

emailDomains = ["yahoo.com", "aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com",
                "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com",
                "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk", "comcast.net", "ymail.com",
                "outlook.com", "cox.net", "rocketmail.com", "sky.com", "optonline.net", "me.com", "mail.com",
                "juno.com", "qq.com", "zoho.com", "inbox.com", "yahoo.com.br", "hotmail.com.br", "email.com",
                "pobox.com", "ygm.com", "safe-mail.net", "gmail.com", "gmail.com", "gmail.com", "gmail.com",
                "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com",
                "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com", "gmail.com",
                "gmail.com", "gmail.com"]

emailIdPostFixes = ["", "", "", "eng", "", "", "", "", "", "", "", "off", "", "", "", "", "", "", "", "", "study", "",
                    "", "", "", "",
                    "", "", "1", "00", "", "", "", "2000", "", "", "", "", "", "", "", "123", "", "", "66", "", "", "",
                    "", "", "",
                    "", "", "learn", "", "", "", "", "22", "", "", "", "", "", "99", "", "", "", "41", "", "work", "",
                    "", "", "", "", "1", "2", "3", "4", "5", "6", "7", "8", "9", "21", "xx", "A1", "in", "usa", ""]

emailIdMidFixes = [".", "_", "-", ".0.", "__", "-_", ".", ".", "1", ".and.", "_0_", "x", ".x1", "", ".us.", ".y."]

connection = pymysql.connect(host='work.ciu1thdpia44.us-east-2.rds.amazonaws.com',
                             user='sujithgeorge',
                             password='hotmail143',
                             db='work',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()


# users fit for current stage
#
#
def getCredsForCurrentStage(runMode):
    print("Entering getCredsForCurrentStage")
    try:
        sql = ""

        if (runMode == 'ENROLMENT'):
            return ("", "")

        if (runMode == 'BROWSE'):
            sql = "SELECT `email` FROM `tasks` where `status`='success' and `stage`='ENROLMENT' order by RAND() limit 1"

        if (runMode == 'WATCHVIDEO'):
            sql = "SELECT `email` FROM `tasks` where `status`='success' and `stage`='BROWSE' order by RAND() limit 1"

        if (runMode == 'SPECIFIC'):
            sql = "SELECT `email` FROM `tasks` where `status`='success' and `stage`='WATCHVIDEO' order by RAND() limit 1"

        cursor.execute(sql)
        result = cursor.fetchall()
        email = result[0]['email']
        sql = "SELECT `passwd` FROM `creds` where `email`='" + email + "' order by RAND() limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        passwd = result[0]['passwd']
        print("Exited getCredsForCurrentStage")
    except Exception as e:
        print("Exception in getCredsForCurrentStage. Returning blank creds")
        return ("", "")
    return (email, passwd)


# before a fresh signup
#
#
def beforeSignUp(driver):
    driver.get("http:///wwww.udemy.com")
    sleep(random.randint(10, 15))

    if random.choice([True, False]):
        browseCategoriesEl = driver.find_element_by_xpath("//a[@id='header.browse']")
        action = ActionChains(driver)
        action.move_to_element(browseCategoriesEl).send_keys(Keys.ALT).perform()
        sleep(random.randint(1, 2))
        firstLevelMenuItems = driver.find_elements_by_xpath(
            "//ul[@class='dropdown-menu__list dropdown-menu__list--level-one']/li")
        firstLevelMenuItemsSize = len(firstLevelMenuItems)
        interestedFirstLevelMenu = firstLevelMenuItems[random.randint(0, firstLevelMenuItemsSize - 1)]
        action = ActionChains(driver)
        action.move_to_element(interestedFirstLevelMenu).send_keys(Keys.ALT).perform()
        sleep(random.randint(4, 5))
        secondLevelMenuItems = driver.find_elements_by_xpath(
            "//ul[@class='dropdown-menu__list dropdown-menu__list--level-two']/li")
        secondLevelMenuItemsSize = len(secondLevelMenuItems)
        interestedSecondLevelMenu = secondLevelMenuItems[random.randint(0, secondLevelMenuItemsSize - 1)]
        action = ActionChains(driver)
        action.move_to_element(interestedSecondLevelMenu).send_keys(Keys.ALT).perform()
        sleep(random.randint(2, 3))
        interestedSecondLevelMenu.click()
        sleep(random.randint(10, 15))
        udemyTopLogoEl = driver.find_element_by_xpath("//img[@class='udemy-logo']")
        driver.execute_script("arguments[0].scrollIntoView();", udemyTopLogoEl)
        udemyTopLogoEl.click()
        sleep(random.randint(10, 15))

    # search using top search field, select one results, look at one course landing page, come back
    if random.choice([True, False]):
        topSearchFieldEl = driver.find_element_by_xpath("//input[@id='header-search-field']")
        action = ActionChains(driver)
        action.move_to_element(topSearchFieldEl).click().perform()
        sleep(1)
        topSearchFieldEl.send_keys(random.choice(searchKeywords))
        topSearchFieldEl.send_keys(Keys.RETURN)
        sleep(random.randint(10, 15))
        searchResults = driver.find_elements_by_xpath("//h4")
        searchResultsSize = len(searchResults)
        interestedResult = searchResults[random.randint(0, searchResultsSize - 1)]
        action = ActionChains(driver)
        driver.execute_script("arguments[0].scrollIntoView();", interestedResult)
        sleep(random.randint(3, 4))
        action.move_to_element(interestedResult).click().perform()
        sleep(random.randint(6, 15))
        udemyTopLogoEl = driver.find_element_by_xpath("//img[@class='udemy-logo']")
        driver.execute_script("arguments[0].scrollIntoView();", udemyTopLogoEl)
        udemyTopLogoEl.click()
        sleep(random.randint(10, 15))

    # scroll down and side scroll through some courses by clicking right arrow button
    if random.choice([True, False]):
        rightArrowElements = driver.find_elements_by_xpath("//button[@class='carousel-arrow next']")
        rightArrowElementsSize = len(rightArrowElements)
        interestedRightArrow = rightArrowElements[random.randint(0, rightArrowElementsSize - 1)]
        driver.execute_script("arguments[0].scrollIntoView();", interestedRightArrow)
        sleep(random.randint(1, 4))
        action = ActionChains(driver)
        action.move_to_element(interestedRightArrow).click().perform()
        sleep(random.randint(10, 15))
        udemyTopLogoEl = driver.find_element_by_xpath("//img[@class='udemy-logo']")
        driver.execute_script("arguments[0].scrollIntoView();", udemyTopLogoEl)
        udemyTopLogoEl.click()
        sleep(random.randint(10, 15))


# for a fresh signup
#
#
def freshSignUp(driver):
    try:
        # TODO
        # beforeSignUp(driver)
        sql = "SELECT `firstname`, `lastname` FROM `names` order by RAND() limit 1"
        cursor.execute(sql)
        result = cursor.fetchall()
        # print(result)
        firstName = result[0]['firstname']
        lastName = result[0]['lastname']
        firstNameAllLower = str.lower(firstName)
        firstNameFirstThree = firstNameAllLower[:2]
        firstNameFirst = firstNameAllLower[0]
        lastNameAllLower = str.lower(lastName)
        lastNameFirstThree = lastNameAllLower[:1]
        lastNameFirst = lastNameAllLower[0]

        selectedFirstNamePart = [firstNameAllLower, firstNameFirstThree, firstNameFirst]
        selectedLastNamePart = [lastNameAllLower, lastNameFirstThree, lastNameFirst]

        combinedEmailId = random.choice(selectedFirstNamePart) + random.choice(
            emailIdMidFixes) + random.choice(selectedLastNamePart) + random.choice(emailIdPostFixes)

        if (len(combinedEmailId) < 8):
            combinedEmailId = combinedEmailId + str(random.randint(10, 99))

        completeEmailId = combinedEmailId + "@" + random.choice(emailDomains)
        combinedName = random.choice(selectedFirstNamePart) + " " + random.choice(
            selectedLastNamePart)

        if (len(combinedName) < 5):
            combinedName = combinedName + firstNameAllLower

        password = random.choice(selectedLastNamePart) + random.choice(emailIdPostFixes) + random.choice(
            emailIdPostFixes) + random.choice(emailIdMidFixes)

        if (len(password) < 6):
            password = password + random.choice(selectedLastNamePart) + random.choice(
                selectedLastNamePart) + random.choice(emailIdPostFixes) + random.choice(selectedFirstNamePart) + 'abc'

        password = password.replace(" ", "")
        completeEmailId = completeEmailId.replace(" ", "")

        completeEmailId = unidecode(completeEmailId)
        password = unidecode(password)

        combinedName.replace("'", "")
        completeEmailId.replace("'", "")
        password.replace("'", "")

        print("Name:" + combinedName)
        print("Email:" + completeEmailId)
        print("Password:" + password)

        driver.get('http://www.udemy.com')
        sleep(random.randint(10, 15))

        # Click Sign up button
        signUpButtonEl = driver.find_element_by_xpath("//button[@data-purpose='header-signup']")
        driver.execute_script("arguments[0].scrollIntoView();", signUpButtonEl)
        action = ActionChains(driver)
        action.move_to_element(signUpButtonEl).click().perform()
        sleep(random.randint(6, 8))
        # Click email signup button - won't be there sometimes
        try:
            emailSignUpButtonEl = driver.find_element_by_xpath("//a[@data-purpose='email-signup-link']")
            driver.execute_script("arguments[0].scrollIntoView();", emailSignUpButtonEl)
            action = ActionChains(driver)
            action.move_to_element(emailSignUpButtonEl).click().perform()
            sleep(random.randint(3, 5))
        except NoSuchElementException:
            print("email signup button not there, so skipping")
        # Fill up fields and submit
        fullNameTextBoxEl = driver.find_element_by_xpath("//input[@name='fullname']")
        fullNameTextBoxEl.click()
        sleep(1)
        fullNameTextBoxEl.send_keys(combinedName)
        sleep(random.randint(2, 5))
        emailTextBoxEl = driver.find_element_by_xpath("//input[@name='email']")
        emailTextBoxEl.click()
        sleep(1)
        emailTextBoxEl.send_keys(completeEmailId)
        sleep(random.randint(2, 5))
        passwordEl = driver.find_element_by_xpath("//input[@name='password']")
        passwordEl.click()
        sleep(1)
        passwordEl.send_keys(password)
        sleep(random.randint(2, 5))

        subscribeEmailsEl = driver.find_element_by_xpath("//input[@data-purpose='subscribe-to-emails']")
        if random.choices([True, False], [85, 15], k=1)[0]:
            driver.execute_script("arguments[0].click();", subscribeEmailsEl)
            sleep(random.randint(2, 5))

        signUpSubmitButtonEl = driver.find_element_by_xpath('//input[@name="submit"]')
        signUpSubmitButtonEl.click()
        sleep(random.randint(10, 15))

        # update newly created creds into RDS
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT into `creds` values('" + combinedName + "','" + completeEmailId + "','" + password + "',now())"
        print("Sql:" + sql)
        cursor.execute(sql)

        sql = "INSERT into `tasks` values('" + completeEmailId + "','ENROLMENT','" + "success" + "',now())"
        print("Sql:" + sql)
        cursor.execute(sql)
        connection.commit()

        # Re-use the browse method. You are signed in now anyways.
        # TODO increase
        for i in range(random.randint(1, 2)):
            memberBrowseAndEnroll(driver)
            if random.choice([True, False]):
                watchVideo(driver)

    except Exception as excp:
        sql = "INSERT into `tasks` values('" + completeEmailId + "','ERROR-ENROLMENT','" + "failed:" + traceback.format_exc().replace(
            "'", '"') + "',now())"
        print("Sql:" + sql)
        cursor.execute(sql)
        connection.commit()


# after signing up
#
#
def memberBrowseAndEnroll(driver):
    driver.get("http://www.udemy.com")
    sleep(random.randint(10, 15))
    # After signinup up, search using top search field, select one results, look at one course landing page, come back
    topSearchFieldEl = driver.find_element_by_xpath("//input[@id='header-search-field']")
    action = ActionChains(driver)
    action.move_to_element(topSearchFieldEl).click().perform()
    sleep(1)
    topSearchFieldEl.send_keys(random.choice(searchKeywords))
    topSearchFieldEl.send_keys(Keys.RETURN)
    sleep(random.randint(10, 15))
    if random.choices([True, False], [95, 5], k=1)[0]:
        filterButtonEl = driver.find_element_by_xpath('//button[contains(@class,"filter")]/span[text()="All Filters"]')
        filterButtonEl.click()
        sleep(random.randint(2, 4))
        englishFilterEl = driver.find_element_by_xpath(
            '//span[contains(@class,"toggle-control")]//span[text()="English"]')
        sleep(random.randint(2, 4))
        driver.execute_script("arguments[0].scrollIntoView();", englishFilterEl)
        driver.execute_script("arguments[0].click();", englishFilterEl)
        freeFilterEl = driver.find_element_by_xpath('//span[contains(@class,"toggle-control")]//span[text()="Free"]')
        driver.execute_script("arguments[0].scrollIntoView();", freeFilterEl)
        driver.execute_script("arguments[0].click();", freeFilterEl)
        sleep(random.randint(2, 4))
        applyButtonEl = driver.find_element_by_xpath('//button[text()="Apply"]')
        driver.execute_script("arguments[0].scrollIntoView();", applyButtonEl)
        applyButtonEl.click()
        sleep(random.randint(10, 15))
    if random.choice([True, False]):
        try:
            nextPage = driver.find_element_by_xpath('//ul[contains(@class,"pagination")]/li/a[contains(text(),2)]')
            driver.execute_script("arguments[0].scrollIntoView();", nextPage)
            nextPage.click()
        except NoSuchElementException:
            print("Page 2 does not exist for this search")
        sleep(random.randint(10, 15))
    searchResults = driver.find_elements_by_xpath("//h4")
    searchResultsSize = len(searchResults)
    interestedResult = searchResults[random.randint(0, searchResultsSize - 1)]
    action = ActionChains(driver)
    driver.execute_script("arguments[0].scrollIntoView();", interestedResult)
    sleep(random.randint(3, 4))
    driver.execute_script("arguments[0].click();", interestedResult)
    sleep(random.randint(5, 10))
    try:
        addToCartEl = driver.find_element_by_xpath("//button[contains(@class,'add-to-cart')]")
        driver.execute_script("arguments[0].scrollIntoView();", addToCartEl)
        addToCartEl.click()
    except NoSuchElementException:
        enrollNowEl = driver.find_element_by_xpath("//button[@data-purpose='buy-this-course-button']")
        driver.execute_script("arguments[0].scrollIntoView();", enrollNowEl)
        enrollNowEl.click()
    sleep(random.randint(10, 15))
    driver.get("http://www.udemy.com")
    sleep(random.randint(10, 15))


# Watch video from among enrolled courses
#
#
def watchVideo(driver):
    driver.get("http://www.udemy.com")
    sleep(random.randint(10, 15))
    myCoursesTopLinkEl = driver.find_element_by_xpath("//a[@id='header.my-courses']")
    myCoursesTopLinkEl.click()
    sleep(random.randint(10, 15))
    listOfEnrolledCourses = driver.find_elements_by_xpath('//div[contains(@class,"card")]//div[@class="play-button"]')
    numEnrolledCoursesInCurrPage = len(listOfEnrolledCourses)
    interestedEnrolledCourse = listOfEnrolledCourses[random.randint(0, numEnrolledCoursesInCurrPage - 1)]
    driver.execute_script("arguments[0].scrollIntoView();", interestedEnrolledCourse)
    try:
        dismissPopupEl = driver.find_element_by_xpath('//small[contains(@ng-click,"dismiss")]')
        dismissPopupEl.click()
        sleep(1)
    except NoSuchElementException:
        print("No angular popup in my course page found")
    # Play course!
    sleep(2)
    driver.execute_script("arguments[0].click();", interestedEnrolledCourse)
    sleep(random.randint(10, 15))
    try:
        modalPopupEl = driver.find_element_by_xpath('//div[contains(@class,"modal")]//button[@class="close"]')
        modalPopupEl.click()
        sleep(1)
    except NoSuchElementException:
        print("No modal window in course play page")

    try:
        initialPlayButton = driver.find_element_by_xpath('//div[contains(@data-purpose,"play-button")]')
        initialPlayButton.click()
    except NoSuchElementException:
        print("Play button not there on play page")
    listOfSectionExpanders = driver.find_elements_by_xpath(
        '//div[contains(@class,"section-heading")]//span[contains(@class,"angle-down")]')
    for sectionExpander in listOfSectionExpanders:
        driver.execute_script("arguments[0].scrollIntoView();", sectionExpander)
        sectionExpander.click()
    try:
        nextVideoRightAngler = driver.find_element_by_xpath('//span[contains(@class,"angle-right")]')
        nextVideoRightAngler.click()
    except NoSuchElementException:
        print("Right next button not present on initial video. Maybe its a quiz or coding exercise?")
    allProgressCheckBoxes = driver.find_elements_by_xpath('//input[@data-purpose="progress-toggle-button"]')
    for progressCheckBox in allProgressCheckBoxes:
        sleep(random.randint(2, 4))
        if random.choice([True, False]):
            driver.execute_script("arguments[0].click();", progressCheckBox)
    try:
        nextVideoRightAngler = driver.find_element_by_xpath('//span[contains(@class,"angle-right")]')
        nextVideoRightAngler.click()
    except NoSuchElementException:
        print("Right next button not present on initial video. Maybe its a quiz or coding exercise?")
    try:
        leaveRatingEl = driver.find_element_by_xpath('//div[contains(@class,"leave-rating")]')
        driver.execute_script("arguments[0].click();", leaveRatingEl)
        sleep(2)

        twoEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-2-label")]')
        twoandhalfEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-2.5-label")]')
        threeEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-3-label")]')
        threeandhalfEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-3.5-label")]')
        fourEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-4-label")]')
        fourandhalfEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-4.5-label")]')
        fiveEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-5-label")]')

        allRatingsList = [twoEl, twoandhalfEl, threeEl, threeandhalfEl, fourEl, fourandhalfEl, fiveEl]
        weightageList = [1, 1, 2, 2, 3, 16, 75]
        ratingToBeGiven = random.choices(allRatingsList, weightageList, k=1)[0]
        if random.choices([True, False], [75, 25], k=1)[0]:
            driver.execute_script("arguments[0].click();", ratingToBeGiven)
    except NoSuchElementException:
        print("Leave rating button not found. Maybe rating already given?")


def login(driver, loginusername, loginpassword):
    driver.get('http://www.udemy.com')
    sleep(random.randint(10, 15))
    # Click Login button
    loginButtonEl = driver.find_element_by_xpath("//button[text()='Log In']")
    driver.execute_script("arguments[0].scrollIntoView();", loginButtonEl)
    action = ActionChains(driver)
    action.move_to_element(loginButtonEl).click().perform()
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


def specificEnroll(driver, specificKeywordList, authorName):
    driver.get("http://www.udemy.com")
    sleep(random.randint(10, 15))
    topSearchFieldEl = driver.find_element_by_xpath("//input[@id='header-search-field']")
    action = ActionChains(driver)
    action.move_to_element(topSearchFieldEl).click().perform()
    sleep(1)
    topSearchFieldEl.send_keys(random.choice(specificKeywordList))
    topSearchFieldEl.send_keys(Keys.RETURN)
    sleep(random.randint(10, 15))
    if random.choice([True, False]):
        filterButtonEl = driver.find_element_by_xpath('//button[contains(@class,"filter")]/span[text()="All Filters"]')
        filterButtonEl.click()
        sleep(random.randint(2, 4))
        englishFilterEl = driver.find_element_by_xpath(
            '//span[contains(@class,"toggle-control")]//span[text()="English"]')
        sleep(random.randint(2, 4))
        driver.execute_script("arguments[0].scrollIntoView();", englishFilterEl)
        driver.execute_script("arguments[0].click();", englishFilterEl)
        freeFilterEl = driver.find_element_by_xpath('//span[contains(@class,"toggle-control")]//span[text()="Free"]')
        driver.execute_script("arguments[0].scrollIntoView();", freeFilterEl)
        driver.execute_script("arguments[0].click();", freeFilterEl)
        sleep(random.randint(2, 4))
        applyButtonEl = driver.find_element_by_xpath('//button[text()="Apply"]')
        driver.execute_script("arguments[0].scrollIntoView();", applyButtonEl)
        applyButtonEl.click()
        sleep(random.randint(10, 15))
    try:
        specificResult = driver.find_element_by_xpath('//span[contains(text(),"By ' + authorName + '")]')
    except NoSuchElementException:
        try:
            nextPage = driver.find_element_by_xpath('//ul[contains(@class,"pagination")]/li/a[contains(text(),2)]')
            driver.execute_script("arguments[0].scrollIntoView();", nextPage)
            nextPage.click()
            sleep(random.randint(10, 15))
            specificResult = driver.find_element_by_xpath('//span[contains(text(),"By ' + authorName + '")]')
        except NoSuchElementException:
            print("Sujith is not there in Page 2 also!")
    action = ActionChains(driver)
    driver.execute_script("arguments[0].scrollIntoView();", specificResult)
    sleep(random.randint(3, 4))
    driver.execute_script("arguments[0].click();", specificResult)
    sleep(random.randint(5, 10))
    enrollNowEl = driver.find_element_by_xpath("//button[@data-purpose='buy-this-course-button']")
    driver.execute_script("arguments[0].scrollIntoView();", enrollNowEl)
    enrollNowEl.click()
    sleep(random.randint(10, 15))
    driver.get("http://www.udemy.com")
    sleep(random.randint(10, 15))


# Watch video from among enrolled courses
#
#
def watchSpecificVideo(driver, authorName):
    driver.get("http://www.udemy.com")
    sleep(random.randint(10, 15))
    myCoursesTopLinkEl = driver.find_element_by_xpath("//a[@id='header.my-courses']")
    myCoursesTopLinkEl.click()
    sleep(random.randint(10, 15))
    try:
        sortByDropDown = driver.find_element_by_xpath('//button[@id="sort-dropdown-label"]')
        driver.execute_script("arguments[0].click();", sortByDropDown)
        sleep(1)
        recentlyEnrolledOption = driver.find_element_by_xpath('//span[text()="Recently Enrolled"]')
        driver.execute_script("arguments[0].click();", recentlyEnrolledOption)
        sleep(random.randint(5, 10))
    except NoSuchElementException:
        print("no sort drop down in 'My Courses'. Too less courses probably.")

    latestEnrolledCourse = driver.find_element_by_xpath('//div[contains(text(),"' + authorName + '")]')
    driver.execute_script("arguments[0].scrollIntoView();", latestEnrolledCourse)
    try:
        dismissPopupEl = driver.find_element_by_xpath('//small[contains(@ng-click,"dismiss")]')
        dismissPopupEl.click()
        sleep(1)
    except NoSuchElementException:
        print("No angular popup in my course page found")
    # Play course!
    sleep(2)
    driver.execute_script("arguments[0].click();", latestEnrolledCourse)
    sleep(random.randint(10, 15))
    try:
        modalPopupEl = driver.find_element_by_xpath('//div[contains(@class,"modal")]//button[@class="close"]')
        modalPopupEl.click()
        sleep(1)
    except NoSuchElementException:
        print("No modal window in course play page")
    initialPlayButton = driver.find_element_by_xpath('//div[contains(@data-purpose,"play-button")]')
    initialPlayButton.click()
    listOfSectionExpanders = driver.find_elements_by_xpath(
        '//div[contains(@class,"section-heading")]//span[contains(@class,"angle-down")]')
    for sectionExpander in listOfSectionExpanders:
        driver.execute_script("arguments[0].scrollIntoView();", sectionExpander)
        sectionExpander.click()
    try:
        nextVideoRightAngler = driver.find_element_by_xpath('//span[contains(@class,"angle-right")]')
        nextVideoRightAngler.click()
    except NoSuchElementException:
        print("Right next button not present on initial video. Maybe its a quiz or coding exercise?")
    allProgressCheckBoxes = driver.find_elements_by_xpath('//input[@data-purpose="progress-toggle-button"]')
    for progressCheckBox in allProgressCheckBoxes:
        sleep(random.randint(2, 4))
        if random.choice([True, False]):
            driver.execute_script("arguments[0].click();", progressCheckBox)
    try:
        nextVideoRightAngler = driver.find_element_by_xpath('//span[contains(@class,"angle-right")]')
        nextVideoRightAngler.click()
    except NoSuchElementException:
        print("Right next button not present on initial video. Maybe its a quiz or coding exercise?")
    try:
        leaveRatingEl = driver.find_element_by_xpath('//div[contains(@class,"leave-rating")]')
        driver.execute_script("arguments[0].click();", leaveRatingEl)
        sleep(2)

        twoEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-2-label")]')
        twoandhalfEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-2.5-label")]')
        threeEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-3-label")]')
        threeandhalfEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-3.5-label")]')
        fourEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-4-label")]')
        fourandhalfEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-4.5-label")]')
        fiveEl = driver.find_element_by_xpath('//label[contains(@data-purpose,"review-star-input-5-label")]')

        allRatingsList = [twoEl, twoandhalfEl, threeEl, threeandhalfEl, fourEl, fourandhalfEl, fiveEl]
        weightageList = [1, 1, 2, 2, 3, 16, 75]
        ratingToBeGiven = random.choices(allRatingsList, weightageList, k=1)[0]
        driver.execute_script("arguments[0].click();", ratingToBeGiven)
    except NoSuchElementException:
        print("Leave rating button not found. Maybe rating already given?")
