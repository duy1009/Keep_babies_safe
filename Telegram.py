from config import *
import telegram
from cv2 import imwrite, resize
from threading import Thread

def send_warning(photo_path=IMG_DG_PATH):
    try:
        bot = telegram.Bot(token=TOKEN)
        bot.send_photo(chat_id= CHAT_ID,photo=open(photo_path, "rb"), caption="Baby Dangerous!!") 
        print("Send Success!")
    except Exception as ex:
        print("Can not send warning! ", ex)

def alertDangerous(img):
    imwrite(IMG_DG_PATH, resize(img, dsize=(920,640), fx=0.2, fy=0.2))
    thread = Thread(target=send_warning(IMG_DG_PATH))
    thread.start()
    return img