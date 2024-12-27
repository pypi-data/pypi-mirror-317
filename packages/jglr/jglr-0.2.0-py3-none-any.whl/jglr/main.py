import pyautogui
from pyautogui import FailSafeException
from datetime import datetime
from datetime import timedelta
import time
import random
from .parserobj import parser
from .validation import argValidator

screenSize = pyautogui.size()
permWidth = screenSize[0]//2
permHieght = screenSize[1]//2


def main():

    args = parser.parse_args()

    if (x := argValidator(args).getString()):
        print(x)
        exit()
    else:
        if (args.till_time):
            args.till_hour = int(args.till_time[:2])
            args.till_minute = int(args.till_time[3:])

        if (args.till_hour or args.till_minute):
            args.till_hour = args.till_hour if args.till_hour else datetime.now().hour
            args.till_minute = args.till_minute if args.till_minute else datetime.now().minute

        if (args.duration_time):
            args.duration_hour = int(args.duration_time[:2])
            args.duration_minute = int(args.duration_time[3:])

        if (args.duration_hour or args.duration_minute):
            args.duration_hour = args.duration_hour if args.duration_hour else datetime.now().hour
            args.duration_minute = args.duration_minute if args.duration_minute else datetime.now().minute

        if not any([args.till_hour, args.till_minute, args.till_time, args.duration_hour, args.duration_minute, args.duration_time]):
            args.duration_hour = 0
            args.duration_minute = 10

        if (any([args.till_time, args.till_hour, args.till_minute]) and (datetime.now() > datetime.now().replace(hour=args.till_hour, minute=args.till_minute))):
            print("timer cant be set into past")
            exit()
        elif (any([args.till_time, args.till_hour, args.till_minute])):
            targetTime = datetime.now().replace(hour=args.till_hour, minute=args.till_minute)
        else:
            targetTime = datetime.now() + timedelta(
                hours=args.duration_hour, minutes=args.duration_minute)

        print(args)
        print(targetTime)

        match args.quadrant:
            case 1:
                offset = [0, 0]
            case 2:
                offset = [permWidth, 0]
            case 3:
                offset = [0, permHieght]
            case 4:
                offset = [permWidth, permHieght]

        # while (datetime.now() != targetTime | pyautogui.position()[]):
        try:
            pyautogui.moveTo(offset[0]+100, offset[1]+100, duration=3)
            pyautogui.click()
            print("screen size ", screenSize)
            print(f"{offset}")
            time.sleep(5)
            pos = pyautogui.position()
            while (datetime.now() < targetTime and not (pos[0] < offset[0] | pos[0] > offset[0] | pos[1] > offset[1] | pos[1] > offset[1])):
                pos = pyautogui.position()
                pyautogui.moveTo(
                    offset[0]+permWidth/2+(permWidth)*random.randint(-5,
                                                                     5)*0.05 + random.randint(-50, 50),
                    offset[1]+permHieght/2+(permHieght)*random.randint(-5,
                                                                       5)*0.03 + random.randint(-30, 30),
                    duration=random.randint(3, 6))
                time.sleep(random.randint(3, 5))
                pyautogui.click()
            print("exiting")
        except FailSafeException:
            print("Edge detected - exiting safely...")
            exit()


if __name__ == "__main__":
    main()
