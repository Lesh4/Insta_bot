""" This program is liking photos in instagram by hashtags"""
from time import sleep
from re import findall
from os import getcwd
from json import load, dump
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


"""
TODO: 

upgrade statistics
----------------------------
I think, that I`ve done this, but IDK:               DONE
so u need to do this:
- download cromedriver.exe
- make dir with exe and program
- show program path to this exe
(do it with os)
----------------------------
also u can add autorun 4 this program
----------------------------
make file with user data                             DONE
----------------------------
add function that will work with hashtags (изменять, удалять, дополнять)
----------------------------
open hashtags stories
"""


def like_buttun_check(driver):
    """ Checking already liked  photos """
    content = driver.find_element_by_class_name('fr66n')
    word_like = r"Нравится"
    like_pointer = findall(
        word_like, content.get_attribute('innerHTML'))
    try:
        if like_pointer[0] == word_like:
            return True
    except:
        return False


def making_data_file():
    """ Make file with user data """
    try:
        user_dict = {}
        with open("data.json", "r") as data:
            user_dict = load(data)
    except FileNotFoundError:
        entering_text = "Привет! Для работы программы мне нужны твои данные: логин и пароль. "
        entering_text += "Внизу ты можешь видеть поле для заполнения\n"
        print(entering_text)
        # user give his data:
        user_dict = {'username': input(
            "ЛОГИН: "), 'password': input("ПАРОЛЬ: ")}
        entering_text2 = '\nСупер! Теперь создадим список с хэштегами, '
        entering_text2 += 'по которым программа будет "ходить".'
        entering_text2 += '\nПишем тег --> нажимаем Enter --> пишем другой. '
        entering_text2 += 'И так пока ты не напишешь: ОК (англ)\n'
        print(entering_text2)
        hashtags = []
        while True:
            input_data = input()
            if input_data.lower() != "ok":
                hashtags.append(input_data)
            else:
                break
        user_dict['hashtags'] = hashtags
        with open("data.json", "w") as data:
            dump(user_dict, data)
    else:
        return user_dict


class InstaBot:
    """This class is for work with browser"""

    def __init__(self, path):
        self.path = path
        self.driver = webdriver.Chrome(self.path + "\\chromedriver.exe")

    def close_browser(self):
        """ Just close the browser """
        self.driver.close()

    def login(self, username, password):
        """ Login user in instagram """
        log_path = "//a[@href='/accounts/login/?source=auth_switcher']"
        user_path = "//input[@name='username']"
        password_path = "//input[@name='password']"
        driver = self.driver
        driver.get("https://www.instagram.com/")
        # driver.maximize_window()
        sleep(4)
        login_button = driver.find_element_by_xpath(log_path)
        login_button.click()
        sleep(2)
        user = driver.find_element_by_xpath(user_path)
        user.clear()
        user.send_keys(username)
        sleep(3)
        password_text = driver.find_element_by_xpath(password_path)
        password_text.clear()
        password_text.send_keys(password)
        password_text.send_keys(Keys.RETURN)
        sleep(2)

    def like(self, hashtag):
        """ Like photos """
        sleep(2)
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        sleep(2)
        # scrolling down
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        sleep(3)

        # scrolling up
        driver.execute_script("scroll(0, 0);")
        sleep(2)

        # searching for pic link
        content_links = driver.find_element_by_css_selector(
            '#react-root > section > main > article > div.EZdmt > div > div')
        a_href = r"/p/.........../"
        links = findall(a_href, content_links.get_attribute('innerHTML'))

        # liking photos
        liked_photos = 0
        unliked_photos = 0
        for link in links:
            sleep(4)
            driver.get("https://www.instagram.com" + link)
            sleep(4)
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)

            # searching for like button
            css_selector = "#react-root > section > main > div > div > article > "
            css_selector += "div.eo2As > section.ltpMr.Slqrh > span.fr66n > button > span"
            button = driver.find_element_by_css_selector(css_selector)

            flag = like_buttun_check(driver)
            if flag:
                liked_photos += 1
                sleep(10)
                button.click()
                sleep(10)
                driver.back()
            else:
                unliked_photos += 1
                sleep(5)
                driver.back()

        print("HASHTAG: ", hashtag, "  Liked: ",
              liked_photos, "  Unliked: ", unliked_photos, "\n")


PATH = getcwd()
USER_DICT = making_data_file()
INSTA_BOT = InstaBot(PATH)
USERNAME = USER_DICT['username']
PASSWORD = USER_DICT['password']
HASHTAGS = USER_DICT['hashtags']
INSTA_BOT.login(USERNAME, PASSWORD)
# hashtags = ["balroomdance",
#"ireland", "films", "calithenics",
# "life", "smile", "relax", "workout", "sport"]
for HASHTAG in HASHTAGS:
    try:
        INSTA_BOT.like(HASHTAG)
    except:
        print("ERROR ", HASHTAG)
        continue
INSTA_BOT.close_browser()
