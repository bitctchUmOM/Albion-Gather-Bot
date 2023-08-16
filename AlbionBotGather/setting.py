print('STARTING APP...')

import json
from time import sleep

import keyboard


config = json.loads(open('config.json').read())



def qexit():
        global running
        running = 0
    
def qexitss():
        global running
        running = 0
 
running = 1


print('''
Текущая конфигурация:''')
print(f'''[+] Точность для определяемого объекта: {config['cnn']}''')
print(f'''[+] Прожимаемые скилы: {config['skills']}''')



keyboard.add_hotkey("alt+s", lambda: qexitss())
keyboard.add_hotkey("alt+p", lambda: qexit())

while running:
    sleep(0.3)