from datetime import datetime, timedelta
import json
from math import sqrt
import os
from PIL import ImageGrab
import keyboard
import numpy as np
import psutil
import pyautogui as pag
import tkinter as tk
from tkinter import messagebox
import cv2
from sys import exit as qx
from time import sleep
import ultralytics
from random import randint

ultralytics.checks()


root = tk.Tk()
root.withdraw()

config          = json.loads(open('config.json').read())
model           = ultralytics.YOLO('best.pt')
scrn            = list(pag.size())
timeout_looting = config["timeout_looting"]
timeout_map     = config["timeout_map"]

pag.FAILSAFE = False

person  = [1280//2, 720//2-30]
system_drive = f"{os.getenv('APPDATA')}\\Skinner"
print(system_drive)
try:
    os.mkdir(system_drive)
except:
    pass

path_screen = '13yolo.jpg'

profile = config["profile"]

img_atack       = cv2.imread(f'atack_{profile}.png')[68:71, 283:295]
img_looting     = cv2.imread(f'looting_{profile}.png')[447:472, 520:530]
img_dange       = cv2.imread('dange.png')[667:691, 350:371]
img_move_zone   = cv2.imread('move_zone.png')[146:150,400:535]

loot_similarity = config["loot_similarity"]
atack_similarity = config["atack_similarity"]


class Bot_API:
    def __init__(self) -> None:
        self.start = 1
        self.skan = 1
        self.use = [    config['skills'][0],
                        [timedelta(0, i) for i in config['skills'][1]]
                   ]
        self.timer = {i : datetime.now() for i in self.use[0]}
        
        self.fight = 0
        self.dviz_arr = {'1':[640,1], '2':[1279,1],'3':[1279,360], '4':[1279,719], '5':[640,719], '6':[1,719], '7':[1,360], '8':[1,1]}
        self.move_position = 1
        self.dviz = self.dviz_arr[str(self.move_position)]
        self.fight_one = 0
        self.looting_one = 0

    def attack_press_skills(self):
        for i in range(len(self.use[0])):
            if datetime.now() - self.timer[self.use[0][i]] > self.use[1][i]:
                pag.press(self.use[0][i])
                self.timer[self.use[0][i]] = datetime.now()

    def scaning(self):
        if self.fight:
            sleep(2)
            self.fight = 0
            self.fight_one = 0
            return False
        screenshot = ImageGrab.grab()
        screenshot.save(path_screen)
        sleep(0.01)
        results = model.predict(path_screen, show = False, save=False, imgsz=(1280, 736), conf=config['cnn'])
        mobs = [[]]
        for r in results:
            for c in r.boxes:
                x=(int(c.xyxy[0][0])+int(c.xyxy[0][2]))//2
                y=(int(c.xyxy[0][1])+int(c.xyxy[0][3]))//2
                mobs[0].append([x, y])

        if mobs[0]:
            x1, y1 = person
            min_distance = 10_000
            nearest_point = None
            for point in range(len(mobs[0])):
                x2, y2 = mobs[0][point][0], mobs[0][point][1]
                distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_point = mobs[0][point]
            pag.click(nearest_point)
            sleep(3)
            if self.atack_or_looting():
                for kol in range(2):
                    pag.click(self.dviz[0], self.dviz[1])
                    sleep(0.6)
                return True
            else: False
        return True
        

    def atack_or_looting(self):
        screenshot = ImageGrab.grab()
        open_cv_image = np.array(screenshot)
        img2 = open_cv_image[:, :, ::-1].copy()
        pixel2 = img2[68:71, 283:295].copy()
        diff = cv2.absdiff(img_atack, pixel2)
        similarity = cv2.mean(diff)[0]
        if int(similarity) <= atack_similarity:
            if self.fight_one == 0:
                self.time_atack = datetime.now()
                self.fight_one = 1
            else:
                if datetime.now() - self.time_atack >= timedelta(0,20):
                    self.move_position = self.move_position+4 if 0<self.move_position<=4 else self.move_position-4 
                    self.dviz = self.dviz_arr[str(self.move_position)]
                    keyboard.press_and_release('alt+s')
                    for kolw in range(5):
                        pag.click(self.dviz[0], self.dviz[1])
                        sleep(0.7) 

                    self.fight_one = 0
                    self.fight = 0
                
            pag.press('space')
            for i in range(len(self.use[0])):
                if datetime.now() - self.timer[self.use[0][i]] > self.use[1][i]:
                    pag.press(self.use[0][i])
                    self.timer[self.use[0][i]] = datetime.now()
            self.fight = 1
            sleep(1.1)
            self.last_scan = datetime.now()
            return False
        else:
            if self.fight:
                self.fight=0
                self.fight_one = 0
                print('unatack')
                sleep(0.3)
                if self.atack_or_looting():
                   sleep(2) 
                else:
                    return False


        pixel2 = img2[447:472, 520:530].copy()
        diff = cv2.absdiff(img_looting, pixel2)
        similarity = cv2.mean(diff)[0]
        if int(similarity) <= loot_similarity:
            if self.looting_one == 0:
                self.looting_one = 1
            
            sleep(timeout_looting)
            self.last_scan = datetime.now()
            return False
        else:
            if self.looting_one:
                self.looting_one = 0
                sleep(0.1)
        return True
    
    def exit_dange(self):
        screenshot = ImageGrab.grab()
        open_cv_image = np.array(screenshot)
        img2 = open_cv_image[:, :, ::-1].copy()
        pixel2 = img2[667:691, 350:371]
        diff = cv2.absdiff(img_dange, pixel2)
        similarity = cv2.mean(diff)[0]
        if int(similarity) <= 9:
            print('dange')
            sleep(2)
            keyboard.press_and_release('a')
            sleep(12)
            self.scrolling()
            pag.moveTo(1150,600)
            self.scrolling()
            pag.moveTo(640,360)
            sleep(1)
            return False
        return True
    
    def check_map(self):
        if datetime.now() - self.last_scan > timedelta(0,timeout_map):
            screenshot = ImageGrab.grab()
            open_cv_image = np.array(screenshot)
            img2 = open_cv_image[:, :, ::-1].copy()
            maper = img2[554:660, 1086:1191]
            diff = cv2.absdiff(maper, self.map)
            similarity = cv2.mean(diff)[0]
            if int(similarity) == 0:
                self.map = maper
                self.reverse_dviz()
                self.last_scan = datetime.now()
            else:
                self.map = maper
                self.last_scan = datetime.now()
                
            diff = cv2.absdiff(img_move_zone, img2[146:150,400:535])
        else:
            screenshot = ImageGrab.grab()
            open_cv_image = np.array(screenshot)
            img2 = open_cv_image[:, :, ::-1].copy()
            diff = cv2.absdiff(img_move_zone, img2[146:150,400:535])
        similarity = cv2.mean(diff)[0]
        if int(similarity) <= 3:
            pag.click(740, 560)
            self.move_position = self.move_position+4 if 0<self.move_position<=4 else self.move_position-4 
            self.dviz = self.dviz_arr[str(self.move_position)] 


    def reverse_dviz(self):
        random_position = randint(1,8)
        while self.move_position == random_position:
            random_position = randint(1,8)
        self.move_position = random_position 
        self.dviz = self.dviz_arr[str(self.move_position)] 
        
    def scrolling(self):
        for i in range(20):
            pag.scroll(1000)
            sleep(0.01)


    def RUN(self):
        os.chdir(system_drive)
        print('START')

        pag.moveTo(640,360)     
        self.scrolling()

        pag.moveTo(1150,600)
        self.scrolling()

        pag.moveTo(640,360)

        screenshot = ImageGrab.grab()
        open_cv_image = np.array(screenshot)
        img2 = open_cv_image[:, :, ::-1].copy()

        self.map = img2[554:660, 1086:1191]
        self.last_scan = datetime.now()
        while 1:
            if self.exit_dange():
                self.check_map()
                if self.atack_or_looting():
                    if self.skaning():
                        pag.click(self.dviz[0], self.dviz[1])

            print(self.fight)
            print(self.fight_one)


bot = Bot_API()
print('APP WAS LOADED')
scrn    = list(pag.size())
processes = psutil.process_iter()
flag = 1

dtnt = [0, 0]

for i in processes:
    if i.name() == 'Albion-Online.exe':
        flag = 0
        dtnt[0] = 1

if scrn!=[1280, 720]:
    messagebox.showerror("Неправильное разрешение экрана",
                                            "Установите разрешение 1280х720")
else:
    dtnt[1] = 1

if flag:
    messagebox.showerror("Запустите игру",
                                            "На данный момент Albion-Online не запущен")
os.system('setting.exe')

if dtnt[0] and dtnt[1]:
    bot.RUN()