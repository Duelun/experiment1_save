import RPi.GPIO as GP
import ablak as ab
import time as ti


obj={}
obj['ablakSzel'] = 1500
obj['ablakMag1'] = 150
obj['ablakMag2'] = 100
obj['ablakMag4'] = 100
obj['ablakMag5'] = 100
obj['schedList']=[0,0]
obj['thermoList'] = [[],['000','001'],['010','011'],['011'],['011','100','101']]
obj['dtData']={'name':['Num','Time','Data A','Data B'],'formats':['u4','f8','i8','i8']}
obj['dtCalc']={'name':['Num','Time','T proc','A/B ea','Sum A/B'], 'formats':['u4','f8','i4','f8','f8']}
obj['colors'] = ['blue','red','magenta2','green3','PeachPuff4','orange']
obj['dataColor'] = {'1':{'A/B ea':'blue','Sum A/B':'red','Data A':'orange','Data B':'magenta2'},
                    '2':{}, '4':{'1':'blue'}, '5':{'A':'blue', 'B':'red'}}

obj['warmTime']=10	#secundum
obj['warmTimeInt']=1	#secundum
obj['dataNum'] = 1000
obj['dataNumInt'] = 1
obj['pixelDraw'] = 1

def presetPin():
    pins={}
    pins['Reset'] = 7
    pins['MintaClkA'] = 11
    pins['MintaClkB'] = 16
    pins['MintaA'] = 13
    pins['MintaB'] = 18
    pins['MintaStart'] = 29
    pins['HomClkA'] = 31
    pins['HomClkB'] = 32
    pins['HomDataA'] = 33
    pins['HomDataB'] = 36
    pins['Out'] = [pins['Reset'],pins['MintaClkA'],pins['MintaClkB'],
                    pins['MintaStart'],pins['HomClkA'],pins['HomClkB']]
    pins['In'] = [pins['MintaA'],pins['MintaB']]
    pins['MintaClk'] = [pins['MintaClkA'], pins['MintaClkB']]
    pins['HomClkS']=[pins['HomClkA'], pins['HomClkB']]
    pins['HomDataS'] = [pins['HomDataA'], pins['HomDataB']]
    
    obj['pins']=pins
    
    GP.setwarnings(False)
    GP.setmode(GP.BOARD)
    GP.setup(obj['pins']['Out'], GP.OUT, initial=GP.LOW)
    GP.setup(obj['pins']['In'], GP.IN, pull_up_down=GP.PUD_DOWN)
    
    GP.setup(obj['pins']['HomDataS'], GP.OUT, initial=GP.HIGH)
    GP.output(obj['pins']['HomClkS'], 1)

presetPin()

ab.ablak(obj)

obj['abl'].mainloop()
#mentes




