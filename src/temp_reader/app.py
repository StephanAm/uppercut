from uppercut.module import Module
from time import time

class TempReadModule(Module):
    def mainLoop(self):
        temp = time() % 60
        self.VarStore.set('temperature',temp)
        print(self)

mod = TempReadModule('TempReadModule',1)

if __name__=="__main__":
    mod.start()