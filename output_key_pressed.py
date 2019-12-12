import fcntl
import os
import sys
import termios

import serial

fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

ser = serial.serial(port='/dev/rfcomm', boudrate=9600)
print(ser.name)

robot_keys = {
    'stop': '#b=0#',
    'forward': '#b=1#',
    'backward': '#b=2#',
    'left': '#b=3#',
    'right': '#b=4#',
    'break0': '#b=9#',
    'break1': '#b=19#',
    'break2': '#b=29#',
    'break3': '#b=39#',
    'break4': '#b=49#',
    'melody': '+DISC',
}

try:
    while 1:
        try:
            c = sys.stdin.read(1)
            if c:
                if c == '\x1b':
                    c2 = sys.stdin.read(2)
                    if c2 == '[A':
                        print("Up")
                        ser.write(robot_keys['forward'])
                    elif c2 == '[B':
                        print("Down")
                        ser.write(robot_keys['backward'])
                    elif c2 == '[C':
                        print("Right")
                        ser.write(robot_keys['right'])
                    elif c2 == '[D':
                        print("Left")
                        ser.write(robot_keys['left'])
                    else:
                        print(f"Don't know this key {c2}")
                else:
                    print("Got character", repr(c))
                    if c == 'b':
                        ser.write(robot_keys['break0'])
                    elif c == 'm':
                        ser.write(robot_keys['melody'])
                    elif c == 'q':
                        break
        except IOError:
            pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
    ser.close()
