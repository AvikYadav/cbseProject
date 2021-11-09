from plyer import notification
from datetime import datetime
from time import sleep
 
def inp():
    inp = [i for i in input('enter values in this format: time,title,message :').split(',')]
    return inp
def time():
    now = datetime.now()
    timenow = now.strftime('%H:%M')
    return timenow

def notificat(title,message):
    notification.notify(
        title =title,
        message = message,
        app_icon = None,
        timeout =10,
    )
Input = inp()
if __name__ == '__main__':
    while True:
        timeN = time()
        if Input[0] == timeN:
            notificat(Input[1],Input[2])
            break
        print(timeN)
        sleep(30)
