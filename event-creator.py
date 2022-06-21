from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from configparser import ConfigParser
import datetime

config = ConfigParser()
config.read("conf.ini")


def create_event(meetup_date, base_url, group_id, username, password):
    driver = webdriver.Chrome()
    driver.get(base_url)

    driver.find_element(By.CLASS_NAME, "UsersAccountMenu-userButton").click()

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.NAME, "action").click()

    driver.get(f"{base_url}/newPost?eventForm=true&groupId={group_id}")

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
    start_time.send_keys(f"{formatted_date} 3:00 PM")

    end_time = driver.find_element(By.NAME, "endTime")
    end_time.click()
    end_time.send_keys(f"{formatted_date} 6:00 PM")

    location = "Garden of the Calouste Gulbenkian Foundation, Avenida de Berna, Lisbon, Portugal"
    driver.find_element(By.XPATH, "//*[@placeholder='Event Location']").send_keys(location)

    contact = "Phone Number: +351960105498"
    driver.find_element(By.XPATH, "//label[text()='Contact Info']/following-sibling::div/input").send_keys(contact)

    driver.find_element(By.XPATH, "//*[text()='Save as draft']").click()


def create_ea_forum_event(meetup_date):
    base_url = "https://forum.effectivealtruism.org"
    group_id = "CojpcGppQzsgPdQaX"
    username = config.get("ea-forum", "email")
    password = config.get("ea-forum", "password")
    create_event(meetup_date, base_url, group_id, username, password)


def create_lesswrong_event(meetup_date):
    base_url = "https://www.lesswrong.com/"
    group_id = "iJzwL2ukGBAGNcwJq"
    username = config.get("lesswrong", "email")
    password = config.get("lesswrong", "password")
    create_event(meetup_date, base_url, group_id, username, password)
    create_event(meetup_date, base_url, group_id)


if __name__ == "__main__":
    meetup_date = datetime.datetime(2022, 7, 16)
    create_ea_forum_event(meetup_date)
    create_lesswrong_event(meetup_date)
