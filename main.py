# -*- coding: utf-8 -*-
import os
import sys
import getpass
from time import sleep
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager as CM
import winreg as reg
import psutil


def isProcessRunning():
    process = "TslGame_BE.exe" # 배그 배틀런쳐

    if any(process in p.name() for p in psutil.process_iter()):
        print(f"[Log] : {process} is running")
    else:
        print(f"[Log] : {process} is not running")

def handle_code_file(filepath, driver):
    with open(filepath, 'r', encoding='cp949') as r:
        code = r.readline().strip()
        print(f"[Log] : Verify Code > {code}")

    ver_code_input = WebDriverWait(driver, 70).until(EC.presence_of_element_located((
        By.XPATH, '/html/body/div/div/div/main/article/div/div/form/div[2]/div/input')))
    ver_code_input.send_keys(code)

    sleep(1)

    WebDriverWait(driver, 70).until(EC.presence_of_element_located((
        By.XPATH, '/html/body/div/div/div/main/article/div/div/form/div[4]/button'))).click()
    print("[Log] : SUCCESS")

    sleep(3)

    WebDriverWait(driver, 70).until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="a_gnb_game_start"]'))).click()
    sleep(1)
    os.remove("code.txt")
    start(driver)

def wait_for_code_file(callback, driver):
    def run():
        while not os.path.exists("code.txt"):
            sleep(1)
        callback("code.txt", driver)
    t = threading.Thread(target=run, daemon=True)
    t.start()

def start(driver):
    WebDriverWait(driver, 70).until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="a_gnb_game_start"]'))).click()
    sleep(1)
    
    import pyautogui

    first_btn_gen = pyautogui.locateAllOnScreen("./asset/2.png",confidence=0.9)
    first_btn = next(first_btn_gen, None)

    second_btn_gen = pyautogui.locateAllOnScreen("./asset/1.png",confidence=0.9)
    second_btn = next(second_btn_gen, None)

    if first_btn:
        pyautogui.click(pyautogui.center(first_btn))
        
        pyautogui.click(pyautogui.center(second_btn))
        print("[Log] : Image Found!")
    else:
        print("[Log] : image Not found :<")
    print("[Log] : driver will terminate in 1 minute")
    sleep(60)
    isProcessRunning()
    driver.quit()

def run_(acc,pw):
    username = getpass.getuser()
    user_data_dir = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/profile-1"

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument("profile-directory=Default")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    
    
    driver.set_window_size(903,696)
    driver.get("https://pubg.game.daum.net/pubg/index.daum")
    try:
        lg_ = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
                By.XPATH, '/html/body/div[1]/div/div[3]/p/a')))
        if lg_:
            start(driver)
        else:
            print("[Log] : Not Found")
    except:
        try:
            already = WebDriverWait(driver, 5).until(EC.presence_of_element_located((
            By.XPATH, '/html/body/div/div/div/main/article/div/div/ul/li[1]/a')))
            if already:
                already.click()
                start()
        except:
            
            print("[Log] : Auto Login Start")
            WebDriverWait(driver, 70).until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="pubGameGGB"]/div/div[3]/a'))).click()
            sleep(3)
            print("s")
            id_input = WebDriverWait(driver, 70).until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="loginId--1"]')))
            id_input.send_keys(acc)
            sleep(1)

            pw_input = WebDriverWait(driver, 70).until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="password--2"]')))
            pw_input.send_keys(pw)
            sleep(1)

            WebDriverWait(driver, 70).until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="label-saveSignedIn"]/span'))).click()
            sleep(1)
            WebDriverWait(driver, 70).until(EC.presence_of_element_located((
                By.XPATH, '//*[@id="mainContent"]/div/div[1]/form/div[4]/button[1]'))).click()

        
            wait_for_code_file(handle_code_file, driver)

            sleep(1000)
        

def ReadIdFile():
    with open("id.txt", 'r') as re:
        ac = re.read()
        acc = ac.split(":")[0]
        pw = ac.split(":")[1]
        
    return {"acc":acc,"pw":pw}

def main():
    ac = ReadIdFile()
    acc = ac["acc"]
    pw = ac["pw"]

    run_(acc,pw)

if __name__ == "__main__":
    main()


#telegram @lee_heyri
