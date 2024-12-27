from argparse import ArgumentParser
import datetime

parser = ArgumentParser(prog="jigl",
                        description='aumated random mouse movements to avoid defualt sleeps',
                        epilog='Only for ethical purposes'
                        )

parser.add_argument("-th", "--till-hour", type=int,
                    help="sets timer till given hour")

parser.add_argument("-tm", "--till-minute", type=int,
                    help="sets timer till given minute")

parser.add_argument("-tt", "--till-time", type=str,
                    help="sets timer till give hh:mm")

parser.add_argument("-q", "--quadrant", type=int, choices=[1, 2, 3, 4], default=4,
                    help="""sets screen size for the mouse movements
Choices: 1 (Top Left), 2 (Top Right), 3 (Bottom Left), 4 (Bottom Right)
default quadrant is 4""")


parser.add_argument("-dh", "--duration-hour", type=int,
                    help="sets duration for mouse movement in hours Max 5 hrs default 0")

parser.add_argument("-dm", "--duration-minute", type=int,
                    help="sets duration for mouse movement in minutes")

parser.add_argument("-dt", "--duration-time", type=str,
                    help="sets duration for mouse movement in hh:mm")
