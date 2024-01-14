import RPi.GPIO as GP
import numpy as np
import time as ti
#from os import getcwd

def clock(w1,clkPin):
    ti.sleep(w1)
    GP.output(clkPin, 1)
    ti.sleep(w1)
    GP.output(clkPin, 0)
    ti.sleep(w1)
def cimTherm(obj, w1, dataPin, clkPin, bites):
    GP.setup(dataPin, GP.OUT, initial=GP.HIGH)
    ti.sleep(w1)
    GP.output(clkPin, 1)
    ti.sleep(w1)
    GP.output(dataPin, 0)
    ti.sleep(w1)
    GP.output(clkPin, 0)
    ti.sleep(w1)
    for b in bites:
        GP.output(dataPin, int(b))
        clock(w1,clkPin)
    GP.setup(dataPin, GP.IN, pull_up_down=GP.PUD_UP)
    ti.sleep(w1)
    GP.output(clkPin, 1)
    ti.sleep(w1)
def readTherm(obj):
    w1=0.000001
    obj['thermReaded'][obj['recordNum']['therm']]['Time'] = ti.time()
    obj['thermReaded'][obj['recordNum']['therm']]['Num'] = obj['recordNum']['therm']
    
    graf1 = obj['T3'].get()
    graf2 = obj['T4'].get()
    if graf1 not in obj['dtTherm']['name'][3:] or graf2 not in obj['dtTherm']['name'][3:]:
        graf1 = ''
        graf2 = ''

    for i, e in enumerate(obj['dtTherm']['name']):
        if i<2:
            continue
        if graf1 != '' and graf2 != '':
            if graf1 != e and graf2 != e:
                obj['thermReaded'][obj['recordNum']['therm']][e] = -1
                if obj['recordNum']['therm'] == 1:
                    obj['thermReaded'][0][e] = obj['thermReaded'][1][e]
                continue
        clkPin=obj['pins']['HomClkS'][int(obj['dtTherm']['board'][i])]
        dataPin=obj['pins']['HomDataS'][int(obj['dtTherm']['board'][i])]
        bites='1001'+obj['dtTherm']['bites'][i]+'1'
        data=''
        cimTherm(obj, w1, dataPin, clkPin, bites)
        hiba = False
        cikl = 5
        while GP.input(dataPin)==1:
            if cikl < 1:
                hiba=True
                break
            cikl -= 1
            ti.sleep(w1*10)
            cimTherm(obj, w1, dataPin, clkPin, bites)
            #continue
        GP.output(clkPin, 0)
        ti.sleep(w1)
        for n in range(8):
            data = data + str(GP.input(dataPin))
            clock(w1,clkPin)
        GP.setup(dataPin, GP.OUT, initial=GP.LOW)
        clock(w1,clkPin)
        GP.setup(dataPin, GP.IN, pull_up_down=GP.PUD_UP)
        ti.sleep(w1)
        for n in range(8):
            data = data + str(GP.input(dataPin))
            clock(w1,clkPin)
        GP.setup(dataPin, GP.OUT, initial=GP.HIGH)
        ti.sleep(w1)
        clock(w1,clkPin)
        ti.sleep(w1)
        GP.output(dataPin, 0)
        ti.sleep(w1)
        GP.output(clkPin, 1)
        ti.sleep(w1)
        GP.output(dataPin, 1)
        obj['thermReaded'][obj['recordNum']['therm']][e] = int(data[1:11], 2)*0.125
        if hiba:
            obj['thermReaded'][obj['recordNum']['therm']][e] = -1
        if obj['recordNum']['therm'] == 1:
            obj['thermReaded'][0][e] = obj['thermReaded'][1][e]
def calcTherm(obj):
    t1 = obj['T1'].get()
    t2 = obj['T2'].get()
    if t1 in obj['thermReaded'][obj['recordNum']['therm']].dtype.names:
        c1 = obj['thermReaded'][obj['recordNum']['therm']][t1]
    else:
        return('none')
    if t2 in obj['thermReaded'][obj['recordNum']['therm']].dtype.names:
        c2 = obj['thermReaded'][obj['recordNum']['therm']][t2]
    else:
        return('none')
    return(c1-c2)
    
def readData(obj):
    w1=0.000001
    obj['dataReaded'][obj['recordNum']['data']]['Num'] = obj['recordNum']['data']
    a1 = ''
    a2 = ''
    i = 47
    obj['dataReaded'][obj['recordNum']['data']]['Time'] = ti.time()
    GP.output(obj['pins']['MintaClk'], 1)
    GP.output(obj['pins']['MintaStart'], 1)
    ti.sleep(w1 * 10)
    while i >= 0:
        GP.output(obj['pins']['MintaClk'], 1)
        ti.sleep(w1)
        if GP.input(obj['pins']['MintaA']):
            a1 = '1' + a1
        else:
            a1 = '0' + a1
        if GP.input(obj['pins']['MintaB']):
            a2 = '1' + a2
        else:
            a2 = '0' + a2
        i -= 1
        GP.output(obj['pins']['MintaClk'], 0)
        ti.sleep(w1)
    GP.output(obj['pins']['MintaStart'], 0)
    
    obj['dataReaded'][obj['recordNum']['data']]['Data A'] = int(a1, 2)
    obj['dataReaded'][obj['recordNum']['data']]['Data B'] = int(a2, 2)

def dataCalc(obj):
    szor = 10000000
    d1 = obj['dataReaded'][obj['recordNum']['data']]['Data A'] - obj['dataReaded'][obj['recordNum']['data']-1]['Data A']
    d2 = obj['dataReaded'][obj['recordNum']['data']]['Data B'] - obj['dataReaded'][obj['recordNum']['data']-1]['Data B']
    obj['dataCalc'][obj['recordNum']['data']]['A/B ea'] = ((d1 / d2) -1) * szor
    d4 = obj['dataReaded'][obj['recordNum']['data']]['Data A']
    d5 = obj['dataReaded'][obj['recordNum']['data']]['Data B']
    obj['dataCalc'][obj['recordNum']['data']]['Sum A/B'] = ((d4 / d5) -1) * szor
    dn = ((d1 - 80000000 * float(obj['sampInt'].get()))/100, (d2 - 80000000 * float(obj['sampInt'].get()))/100)
    return(dn)
    
def presetTherms(obj):
    #homerok alapbeallitas
    #kikapcs nemhasznalt
    #hasznaltra beallit sample time ????
    return




