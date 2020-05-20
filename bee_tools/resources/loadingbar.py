import time
import sys
from time import sleep

class bar:
    def __init__(self,le):
        self.blen = le
        self.txt = ""
        self.perc = 0
    def begin(self):
        sys.stdout.write(f"[{'-'*self.blen}]")
        sys.stdout.flush()
        sys.stdout.write("\b")
    def setbar(self,perc):
        self.perc = perc
        sys.stdout.write("\by\b"*int(self.blen))
        sys.stdout.flush()
        sys.stdout.write("█"*int(self.blen*perc/100))
        sys.stdout.write("-"*(self.blen-int(self.blen*perc/100))+"] "+self.txt)
        sys.stdout.write("\b"*(len(self.txt)+2))
        sys.stdout.flush()
        sleep(0.1)
    def settext(self,txt):
        self.txt = txt
        self.setbar(self.perc)
    def end(self):
        sleep(0.1)
        sys.stdout.write("]\n")
