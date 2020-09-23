from message_handler import MessageHandler
import time
from lmsdriver import LmsDriver

if __name__ == '__main__':

     message_handler = MessageHandler('111')
     while True:
         message_handler.get_message()
         time.sleep(1)
