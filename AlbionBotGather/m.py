# from time import sleep
# import pyautogui as pag
# from random import randint

# while 1:
#     pag.moveTo(randint(100,1400),randint(100,900),2, pag.easeOutQuad)
#     sleep(randint(5,15)/10)
#     pag.scroll(randint(800,1100) if randint(0,1) else -randint(800,1100))
#     sleep(randint(5,15))

import cv2
g1 = cv2.imread('looting_1.png')[447:472, 520:530]
g2 = cv2.imread('looting_3.png')[447:472, 520:530]
diff = cv2.absdiff(g1, g2)
similarity = cv2.mean(diff)[0]
print(similarity)
cv2.imwrite('32.png', g1)
cv2.imwrite('33.png', g2)