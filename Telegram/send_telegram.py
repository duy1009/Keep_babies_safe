import telegram

def send_warning(photo_path="alert.png"):
    try:
        bot = telegram.Bot(token='5811380057:AAG9duwWycJIukxAFeJ98m01wJjgHQEg_2s')
        bot.send_photo(chat_id='5923323553',photo=open(photo_path, "rb"), caption="Baby Dangerous!!") 
        print("Send Success!")
    except Exception as ex:
        print("Can not send warning! ", ex)

