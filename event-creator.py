from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from configparser import ConfigParser
import datetime

config = ConfigParser()
config.read("conf.ini")


def create_event(meetup_date, base_url, group_id, username, password, type):
    driver = webdriver.Chrome()

    if type == "ea":
        driver.get(base_url)
        driver.find_element(By.CLASS_NAME, "UsersAccountMenu-userButton").click()
    elif type == "lw":
        driver.get("https://www.lesswrong.com/login")

    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)

    if type == "ea":
        driver.find_element(By.NAME, "action").click()
    elif type == "lw":
        driver.find_element(By.CLASS_NAME, "WrappedLoginForm-submit").click()
        sleep(5)

    driver.get(f"{base_url}/newPost?eventForm=true&groupId={group_id}")

    sleep(5)

    title = f"ACX/EA Lisbon {meetup_date.strftime('%B')} {meetup_date.year} Meetup"
    driver.find_element(By.XPATH, "//*[@placeholder='Title']").send_keys(title)

    description = ("Exact location: https://plus.codes/8CCGPRJW+V8\n"
                   "In Jardim Amália Rodrigues, close to Linha d'Água cafe, in the top of a hill, below a bunch of "
                   "trees.")
    driver.find_element(By.XPATH, "//*[@aria-label='Rich Text Editor, main']").send_keys(description)

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

    location = "Jardim Amália Rodrigues, Lisbon"
    driver.find_element(By.XPATH, "//*[@placeholder='Event Location']").send_keys(location)
    sleep(1)
    driver.find_element(By.CLASS_NAME, "geosuggest__item").click()

    contact = "Phone Number: +351960105498"
    driver.find_element(By.XPATH, "//label[text()='Contact Info']/following-sibling::div/input").send_keys(contact)

    if type == 'lw':
        for cat in ['LW', 'SSC', 'EA']:
            driver.find_element(By.XPATH, f"//span[text()='{cat}']").click()

    driver.find_element(By.XPATH, "//*[text()='Save as draft']").click()
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
    meetup_date = datetime.datetime(2022, 10, 8)
    create_ea_forum_event(meetup_date)
    create_lesswrong_event(meetup_date)
