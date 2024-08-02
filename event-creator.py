import datetime
from configparser import ConfigParser
from time import sleep

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

config = ConfigParser()
config.read("conf.ini")


def create_event(meetup_date, base_url, group_id, username, password, type):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    if type == "ea":
        driver.get(base_url)
        driver.find_element(By.CLASS_NAME, "UsersAccountMenu-login").click()
        driver.find_element(By.XPATH, "//*[@placeholder='Email']").send_keys(username)
        driver.find_element(By.XPATH, "//*[@placeholder='Password']").send_keys(password)
        print("For some mysterious reason I have to manually click the login button")
    elif type == "lw":
        driver.get("https://www.lesswrong.com/login")
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CLASS_NAME, "LoginForm-submit").click()

    sleep(5)

    driver.get(f"{base_url}/newPost?eventForm=true&groupId={group_id}")

    sleep(5)

    try:
        agreement_checkbox_xpath = "//*[contains(text(), 'Before you can publish this post you must agree to " \
                                   "the')]/../*[1] "
        driver.find_element(By.XPATH, agreement_checkbox_xpath).click()
    except NoSuchElementException:
        pass

    title = f"ACX/EA Lisbon {meetup_date.strftime('%B')} {meetup_date.year} Meetup"
    driver.find_element(By.XPATH, "//*[@placeholder='Event name']").send_keys(title)

    try:
        driver.find_element(By.XPATH, "//span[text()='Accept all']").click()
    except NoSuchElementException:
        pass

    description = (
        "Please don’t feel like you “won’t be welcome” just because you’re new to ACX/EA or demographically different "
        "from the average attendee. You'll be fine!\n"
        "Exact location: https://plus.codes/8CCGPRJW+V8\n"
        "We meet on top of a small hill East of the Linha d'Água café in Jardim Amália Rodrigues. For comfort, bring "
        "sunglasses and a blanket to sit on. There is some natural shade. Also, it can get quite windy, so bring "
        "a jacket.\n"
        "(Location might change due to weather)")

    # description = (
    #     "Please don’t feel like you “won’t be welcome” just because you’re new to ACX/EA or demographically different "
    #     "from the average attendee. You'll be fine!\n"
    #     "We'll meet in Docel: https://goo.gl/maps/39vAg1wjuj7FapMv9"
    # )

    driver.find_element(By.XPATH, "//*[@aria-label='Rich Text Editor. Editing area: main. Press ⌥0 for help.']").send_keys(description)

    driver.find_element(By.XPATH, "//label[text()='Event Format']/following-sibling::div").click()
    driver.find_element(By.XPATH, "//li[text()='Social']").click()

    sleep(5)

    formatted_date = meetup_date.strftime("%m/%d/%Y")
    start_time = driver.find_element(By.NAME, "startTime")
    start_time.click()
    start_time.send_keys(f"{formatted_date} 3:00 PM")

    end_time = driver.find_element(By.NAME, "endTime")
    end_time.click()
    end_time.send_keys(f"{formatted_date} 6:00 PM")

    location = "PRJW+V8 Lisboa, Portugal"
    # location = "docel,"

    driver.find_element(By.XPATH, "//*[@placeholder='Event Location']").send_keys(location)
    sleep(1)
    driver.find_element(By.CLASS_NAME, "geosuggest__item").click()

    contact = "Phone Number: +351960105498"
    driver.find_element(By.XPATH, "//label[text()='Contact Info']/following-sibling::div/input").send_keys(contact)

    if type == 'lw':
        for cat in ['LW', 'SSC', 'EA']:
            driver.find_element(By.XPATH, f"//span[text()='{cat}']").click()

    driver.find_element(By.XPATH, "//*[text()='Submit']").click()
    sleep(2)


def create_ea_forum_event(meetup_date):
    base_url = "https://forum.effectivealtruism.org"
    group_id = "CojpcGppQzsgPdQaX"
    username = config.get("ea-forum", "email")
    password = config.get("ea-forum", "password")
    create_event(meetup_date, base_url, group_id, username, password, "ea")


def create_lesswrong_event(meetup_date):
    base_url = "https://www.lesswrong.com"
    group_id = "iJzwL2ukGBAGNcwJq"
    username = config.get("lesswrong", "email")
    password = config.get("lesswrong", "password")
    create_event(meetup_date, base_url, group_id, username, password, "lw")


if __name__ == "__main__":
    meetup_date = datetime.datetime(2024, 8, 24)
    create_ea_forum_event(meetup_date)
    create_lesswrong_event(meetup_date)
