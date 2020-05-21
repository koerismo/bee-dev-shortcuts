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
    def setbar(self,perc,txt=None):
        if txt:
            sys.stdout.write(" "*(len(self.txt)+2))
            sys.stdout.write("\b"*(len(self.txt)+2))
            self.txt = txt
        self.perc = perc
        sys.stdout.write("\b"*int(self.blen))
        sys.stdout.flush()
        sys.stdout.write("█"*int(self.blen*perc/100))
        sys.stdout.write("-"*(self.blen-int(self.blen*perc/100))+"] "+self.txt)
        sys.stdout.write("\b"*(len(self.txt)+2))
        sys.stdout.flush()
    def settext(self,txt):
        self.setbar(self.perc,txt)
        #self.txt = txt
    def end(self):
        sleep(0.1)
        sys.stdout.write("]\n\n")
        sys.stdout.flush()
