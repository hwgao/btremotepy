import fcntl
import os
import sys
import termios

fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

try:
    while 1:
        try:
            c = sys.stdin.read(1)
            if c:
                if c == '\x1b':
                    c2 = sys.stdin.read(2)
                    if c2 == '[A':
                        print("Up")
                    elif c2 == '[B':
                        print("Down")
                    elif c2 == '[C':
                        print("Right")
                    elif c2 == '[D':
                        print("Left")
                    else:
                        print(f"Don't know this key {c2}")
                else:
                    print("Got character", repr(c))
        except IOError:
            pass
finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
