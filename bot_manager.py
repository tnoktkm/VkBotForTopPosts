from bot import Bot
from config import token_app, token_group, id_group
import time


botDecan = Bot(token_app, token_group, id_group, "BotDecan")

while True:
    try:
        botDecan.start()
    except Exception as e:
        print("***************************************************")
        print("*******Something went wrong.....*******************")
        print(e)
        print("***************************************************")
        with open(f'errors.txt', 'a') as file:
                        file.write(str(e) + "\n")
        time.sleep(60)

