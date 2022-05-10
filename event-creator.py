from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from configparser import ConfigParser

config = ConfigParser()
config.read("conf.ini")


def create_ea_forum_event(month, year):
    driver = webdriver.Chrome()
    driver.get("https://forum.effectivealtruism.org/")

    driver.find_element(By.CLASS_NAME, "UsersAccountMenu-userButton").click()

    driver.find_element(By.ID, "username").send_keys(config.get("ea-forum", "email"))
    driver.find_element(By.ID, "password").send_keys(config.get("ea-forum", "password"))
    driver.find_element(By.NAME, "action").click()

    driver.get("https://forum.effectivealtruism.org/newPost?eventForm=true&groupId=CojpcGppQzsgPdQaX")

    title = f"ACX/EA Lisbon {month} {year} Meetup"
    driver.find_element(By.XPATH, "//*[@placeholder='Title']").send_keys(title)

    description = ("Exact location: https://plus.codes/8CCGPRPW+WF\n"
                    "In the grassy hill over the the lake, close to 'Cafetaria do Museu Gulbenkian'.")
    driver.find_element(By.XPATH, "//*[@aria-label='Rich Text Editor, main']").send_keys(description)







    sleep(22345354)


if __name__ == "__main__":
    create_ea_forum_event(2022, "June")
