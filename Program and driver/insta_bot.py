""" This program is liking photos in instagram by hashtags"""
from time import sleep
from re import findall
from os import getcwd
from json import load, dump
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

entering_text3 = 'Пишем тег --> нажимаем Enter --> пишем другой.\n'
entering_text3 += 'И так пока ты не напишешь: ok (англ)\n'



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
        entering_text = "\nПривет! Для работы программы мне нужны твои данные: логин и пароль. "
        entering_text += "Внизу ты можешь видеть поле для заполнения\n"
        print(entering_text)
        # user gives his data:
        user_dict = {'username': input(
            "ЛОГИН: "), 'password': input("ПАРОЛЬ: ")}
        entering_text2 = '\nСупер! Теперь создадим список с хэштегами, '
        entering_text2 += 'по которым программа будет "ходить".\n'
        print(entering_text2 + entering_text3)
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
        return user_dict
    else:
        return user_dict

def work_with_hashtags():
    """ Changing list of hashtags """
    try:
        with open("data.json", "r") as data:
            user_dict = load(data)
            print("Вот твои хэштеги:")
            print(user_dict['hashtags'])
        print("Хочешь что-то поменять? Ответь да или нет\n")
    except:
        making_data_file()
    else:
        while True:
            answer = input("да/нет >  ")
            if answer.lower() == 'да' or answer.lower() == 'нет':
                break
        if answer.lower() == 'да':
            print("Итак, что ты хочешь сделать?\n")
            print("1) Изменить список хэштегов полностью\n")
            print("2) Добавить хэштег\n")
            print("3) Поменять какой-то хэштег\n")
            print("4) Случайно попал сюда? Ничего, просто напиши 4")
            while True:
                try:
                    number = int(input("\nНапиши номер: "))
                except ValueError:
                    print("Номер пожалуйста)")
                else:
                    break
            hashtags = []
            if number == 1:
                print("\nМожешь писать новые хэштеги.\n")
                print(entering_text3)
                while True:
                    input_data = input()
                    if input_data.lower() != "ok":
                        hashtags.append(input_data)
                    else:
                        break
                user_dict['hashtags'] = hashtags
                with open("data.json", "w") as data:
                    dump(user_dict, data)
                print("Список хэштегов обновлен.")
                work_with_hashtags()
            elif number == 2:
                print("\nДобавляй сколько хочешь, мне не жалко!\n")
                print(entering_text3)
                previous_hashtags = user_dict['hashtags']
                while True:
                    input_data = input()
                    if input_data.lower() != "ok":
                        hashtags.append(input_data)
                    else:
                        break
                hashtags += previous_hashtags
                user_dict.update({'hashtags': hashtags})
                with open("data.json", "w") as data:
                    dump(user_dict, data)
                print("Список хэштегов изменен.")
                work_with_hashtags()
            elif number == 3:
                while True:
                    word = input("Какой хэштег ты хочешь изменить? Напиши его\n")
                    print("Будет сделано!\n")
                    hashtags = user_dict['hashtags']
                    try:
                        hashtags.remove(word)
                    except ValueError:
                        print("Ой! Такого хэштега нет( Возможно ты ошибся\n")
                        print("Нипиши ещё раз")
                    else:
                        break
                print("Хэштег удален!\n")
                print(hashtags)
                print("\nТеперь напиши на какой ты хочешь его поменять:\n")
                word = input("> ")
                hashtags.append(word)
                user_dict.update({'hashtags': hashtags})
                with open("data.json", "w") as data:
                    dump(user_dict, data)
                print("Список хэштегов изменен.")
                work_with_hashtags()
            else:
                pass
        else:
            print("Список хэштегов остается прежним\n")



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
            button = driver.find_element_by_class_name('fr66n')
            
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
work_with_hashtags()
USER_DICT = making_data_file()
USERNAME = USER_DICT['username']
PASSWORD = USER_DICT['password']
HASHTAGS = USER_DICT['hashtags']
sleep(3)
INSTA_BOT = InstaBot(PATH)
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