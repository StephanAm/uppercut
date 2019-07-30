from uppercut.sharedvars import SharedVarStore
from uppercut.module import Module

tempReader = SharedVarStore('TempReadModule')
class TempControlModule(Module):
    def getElementState(self,currentTemp,targetTemp,isOn):
        if isOn and targetTemp and currentTemp:
            return currentTemp < targetTemp
        return False

    def mainLoop(self):
        temperature = tempReader.get('temperature')
        isOn = self.VarStore.get('isOn',False)
        setTemperature = self.VarStore.get('setTemperature')
        elementOn = self.getElementState(temperature,setTemperature,isOn)
        self.VarStore.set('elementOn',elementOn)

tempControlModule = TempControlModule('TempControl',1)

if __name__=='__main__':
    tempControlModule.start()
