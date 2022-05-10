from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from configparser import ConfigParser
import datetime

config = ConfigParser()
config.read("conf.ini")


def create_ea_forum_event(meetup_date):
    driver = webdriver.Chrome()
    driver.get("https://forum.effectivealtruism.org/")

    driver.find_element(By.CLASS_NAME, "UsersAccountMenu-userButton").click()

    driver.find_element(By.ID, "username").send_keys(config.get("ea-forum", "email"))
    driver.find_element(By.ID, "password").send_keys(config.get("ea-forum", "password"))
    driver.find_element(By.NAME, "action").click()

    driver.get("https://forum.effectivealtruism.org/newPost?eventForm=true&groupId=CojpcGppQzsgPdQaX")

    sleep(1)

    title = f"ACX/EA Lisbon {meetup_date.strftime('%B')} {meetup_date.year} Meetup"
    driver.find_element(By.XPATH, "//*[@placeholder='Title']").send_keys(title)

    description = ("Exact location: https://plus.codes/8CCGPRPW+WF\n"
                   "In the grassy hill over the the lake, close to 'Cafetaria do Museu Gulbenkian'.")
    driver.find_element(By.XPATH, "//*[@aria-label='Rich Text Editor, main']").send_keys(description)

    driver.find_element(By.XPATH, "//label[text()='Event Format']/following-sibling::div").click()
    driver.find_element(By.XPATH, "//li[text()='Social']").click()

    formatted_date = meetup_date.strftime("%m/%d/%Y")
    start_time = driver.find_element(By.NAME, "startTime")
    start_time.click()
    start_time.send_keys(f"{formatted_date} 15:00")

    end_time = driver.find_element(By.NAME, "endTime")
    end_time.click()
    end_time.send_keys(f"{formatted_date} 18:00")

    sleep(123)


if __name__ == "__main__":
    meetup_date = datetime.datetime(2022, 6, 22)
    create_ea_forum_event(meetup_date)
