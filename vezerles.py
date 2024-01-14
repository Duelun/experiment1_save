import numpy as np
import RPi.GPIO as GP
import time as ti
import threading as th
import sched as sc
import board_functions as bf
import draw_functions as dr
import file as fi


def setDataArrays(obj, tip):
    obj['startTime']=ti.gmtime()
    if tip == 'read':
        n1=int(obj['sampNum'].get()) + 2
        n2=int(obj['sampNum'].get()) + 2
        obj['dataReaded']=np.zeros(n1,dtype={'names':obj['dtData']['name'],
                                            'formats':obj['dtData']['formats']})
        obj['dataCalc']=np.zeros(n1,dtype={'names':obj['dtCalc']['name'],
                                            'formats':obj['dtCalc']['formats']})
    elif tip == 'warm':
        n2=int(float(obj['wt'].get()) // float(obj['wti'].get())) + 2
    
    obj['recordNum'] = {'data':0, 'therm':0}
    obj['dtTherm']={}
    obj['dtTherm']['name']=['Num','Time']
    obj['dtTherm']['formats']=['i4','f8']
    obj['dtTherm']['board']=['','']
    obj['dtTherm']['bites']=['','']
    ca=obj['thermoList'][int(obj['chA'].get())]
    cb=obj['thermoList'][int(obj['chB'].get())]
    an=len(ca)
    bn=len(cb)
    obj['dataColor']['2'] = {}
    for i in range(1,7):
        obj['fejlectext'+str(i)].set('')
    for i in range(1,an+1):
        tx='C* A'+str(i)
        obj['dataColor']['2'][tx] = obj['colors'][i-1]
        obj['fejlectext'+str(i)].set(tx)
        obj['fejlec'+str(i)].config(fg = obj['colors'][i-1])
        obj['dtTherm']['name']=obj['dtTherm']['name']+[tx]
        obj['dtTherm']['formats']=obj['dtTherm']['formats']+['f4']
        obj['dtTherm']['board']=obj['dtTherm']['board']+['0']
        obj['dtTherm']['bites']=obj['dtTherm']['bites']+[ca[i-1]]
    for i in range(1,bn+1):
        tx='C* B'+str(i)
        obj['dataColor']['2'][tx] = obj['colors'][an+i-1]
        obj['fejlectext'+str(an+i)].set(tx)
        obj['fejlec'+str(an+i)].config(fg = obj['colors'][an+i-1])
        obj['dtTherm']['name']=obj['dtTherm']['name']+[tx]
        obj['dtTherm']['formats']=obj['dtTherm']['formats']+['f4']
        obj['dtTherm']['board']=obj['dtTherm']['board']+['1']
        obj['dtTherm']['bites']=obj['dtTherm']['bites']+[cb[i-1]]
    obj['thermReaded']=np.zeros(n2,dtype={'names':obj['dtTherm']['name'],
                                        'formats':obj['dtTherm']['formats']})

#########
def therm(obj, tip=0):
    #print('start 0  ',ti.time())
    if tip == 1:
        obj['recordNum']['therm'] +=1
        if obj['recordNum']['therm'] == 1:
            obj['thermReaded']['Time'][0] = ti.time()
        t = obj['thermReaded']['Time'][0] + obj['recordNum']['therm'] * float(obj['wti'].get())
        obj['schedList'][1] = obj['scheduler'].enterabs(t, 1, therm, (obj, 1,))
        bf.readTherm(obj)
    
    d=[]
    datas=[]
    name=[]
    result = obj['thermReaded'][obj['recordNum']['therm']]
    for i, e in enumerate(result):
        if i==0:
            obj['labTextvar'][obj['labPointer'][0]].set(e)
            d = [e]
        elif i==1:
            obj['labTextvar'][obj['labPointer'][1]].set(str("{:.6f}".format(e)))
            d = d + [e]
        else:
            obj['labTextvar'][obj['labPointer'][2+i]].set(str("{:.2f}".format(e)))
            if e > -1:
                datas = datas + [e]
                name = name + [obj['thermReaded'].dtype.names[i]]
    if obj['cButDatas'].get()=='1':
        shiftDatas(obj)
    else:
        for i in range(15):
            obj['labTextvar'][obj['labPointer'][i]].set('')
    if obj['cButDraw'].get()=='1':
        if 'C* A2' in name:
            nn = name.index('C* A2')
            del name[nn]
            del datas[nn]
        if 'C* B2' in name:
            nn = name.index('C* B2')
            del name[nn]
            del datas[nn]
        dr.draw(obj, d, datas, name, '2')
        
        result = bf.calcTherm(obj)
        if result != 'none':
            datas = [result]
            name = ['DC*']
            dr.draw(obj, d, datas, name, '4')
    
    obj['labTextvar'][obj['labPointer'][161]].set(str(int((ti.time() - obj['thermReaded'][obj['recordNum']['therm']]['Time'])*1000)))

def warmFinis(obj):
    GP.output(obj['pins']['Reset'], 0)
    obj['scheduler'].cancel(obj['schedList'][1])
    if obj['gomb1'].cget('text') == 'StopReadWarm':
        obj['gomb1Text'].set('StopRead')
        readStart(obj)
    elif obj['gomb1'].cget('text') == 'StopWarm':
        stop(obj)
def warmStart(obj):
    GP.output(obj['pins']['Reset'], 1)
    
    setDataArrays(obj, 'warm')
    dr.canvasPreset(obj)

    obj['scheduler']=sc.scheduler(ti.time, ti.sleep)
    obj['schedList'][0]=obj['scheduler'].enter(float(obj['wt'].get()), 1, warmFinis, (obj,))
    obj['schedList'][1]=obj['scheduler'].enter(0.1, 2, therm, (obj, 1,))
    t0=th.Thread(target=obj['scheduler'].run)
    t0.start()
##########
def data(obj):
    obj['recordNum']['data'] +=1
    if obj['recordNum']['data'] == 1:
        obj['dataReaded']['Time'][0] = ti.time()
    t = obj['dataReaded']['Time'][0] + obj['recordNum']['data'] * float(obj['sampInt'].get())
    obj['schedList'][0] = obj['scheduler'].enterabs(t, 1, data, (obj,))
    
    bf.readData(obj)
    obj['recordNum']['therm'] +=1
    bf.readTherm(obj)
    
    if obj['recordNum']['data'] > 1:
        dn = bf.dataCalc(obj)
        if obj['cButDraw'].get()=='1':
            d = [obj['recordNum']['data'], obj['dataReaded'][obj['recordNum']['data']]['Time']]
            datas = [obj['dataCalc'][obj['recordNum']['data']]['A/B ea']]#, obj['dataCalc'][obj['recordNum']['data']]['Sum A/B']]
            name = ['A/B ea']#, 'Sum A/B']
            dr.draw(obj, d, datas, name, '1')
            
            datas = dn
            name = ['A', 'B']
###            #dr.drawBar(obj, d, datas, name, '5')
            
        if obj['cButDatas'].get()=='1':
            obj['labTextvar'][obj['labPointer'][0]].set(obj['recordNum']['data'])
            obj['labTextvar'][obj['labPointer'][1]].set(str("{:.6f}".format(obj['dataReaded'][obj['recordNum']['data']]['Time'])))
            obj['labTextvar'][obj['labPointer'][2]].set(str(obj['dataReaded'][obj['recordNum']['data']]['Data A']))
            obj['labTextvar'][obj['labPointer'][3]].set(str(obj['dataReaded'][obj['recordNum']['data']]['Data B']))
            obj['labTextvar'][obj['labPointer'][12]].set(str("{:.3f}".format(obj['dataCalc'][obj['recordNum']['data']]['A/B ea'])))
            obj['labTextvar'][obj['labPointer'][13]].set(str("{:.3f}".format(obj['dataCalc'][obj['recordNum']['data']]['Sum A/B'])))
            shiftDatas(obj)
            obj['labTextvar'][obj['labPointer'][161]].set(str(int((ti.time() - obj['dataReaded'][obj['recordNum']['data']]['Time'])*1000)))
    
    therm(obj)
    
    if obj['recordNum']['data'] > int(obj['sampNum'].get()):
        stop(obj)
    
def readStart(obj):
    if int(obj['multiReadTarg'].get()) < 2:
        obj['multiReadTarg'].set('1')
        obj['multiReadAct']['text'] = '1'
    GP.output(obj['pins']['Reset'], 1)
    setDataArrays(obj, 'read')
    dr.canvasPreset(obj)
    dr.clearAblak(obj)
    obj['abl'].update()
    ti.sleep(1)
    
    obj['scheduler']=sc.scheduler(ti.time, ti.sleep)
    obj['schedList'][0]=obj['scheduler'].enter(0, 1, data, (obj,))
    #obj['schedList'][1]=obj['scheduler'].enter(0.3, 2, therm, (obj,))
    t0=th.Thread(target=obj['scheduler'].run)
    t0.start()
    
##########
def stop(obj):
    GP.output(obj['pins']['Reset'], 0)
    
    for s in obj['schedList']:
        try:
            obj['scheduler'].cancel(s)
        except:
            print(' schedul torles hiba ****')
    
    if obj['gomb1Text'].get() == 'StopRead':
        fi.save(obj)
    
    act = int(obj['multiReadAct']['text']) + 1
    if act <= int(obj['multiReadTarg'].get()):
        obj['multiReadAct']['text'] = str(act)
        readStart(obj)
    else:
        obj['multiReadTarg'].set('1')
        obj['multiReadAct']['text'] = '1'
        
        obj['chA'].configure(state='normal')
        obj['chB'].configure(state='normal')
        obj['sampNum'].configure(state='normal')
        obj['sampInt'].configure(state='normal')
        obj['gomb3'].configure(state='normal')
        obj['gomb2'].configure(state='disabled')
        obj['gomb1Text'].set('Start')
        obj['cBut1'].configure(state='normal')
        obj['wt'].configure(state='normal')
        obj['wti'].configure(state='normal')
        obj['mr'].configure(state='normal')
    
def start(obj):
    obj['chA'].configure(state='readonly')
    obj['chB'].configure(state='readonly')
    obj['sampNum'].configure(state='readonly')
    obj['sampInt'].configure(state='readonly')
    obj['gomb3'].configure(state='disabled')
    obj['gomb2'].configure(state='normal')
    obj['cBut1'].configure(state='disabled')
    obj['wt'].configure(state='readonly')
    obj['wti'].configure(state='readonly')
    obj['mr'].configure(state='readonly')
    
    dr.clearAblak(obj)
    #bf.presetTherms(obj)
    
    if obj['sampNum'].get() > '0':
        if obj['cButWarm'].get()=='1':
            obj['cButWarm'].set('0')
            obj['gomb1Text'].set('StopReadWarm')
            warmStart(obj)
        else:
            obj['gomb1Text'].set('StopRead')
            readStart(obj)
    else:	#sampnum=0
        if obj['cButWarm'].get()=='1':
            obj['gomb1Text'].set('StopWarm')
            warmStart(obj)
        else:
            obj['gomb1Text'].set('Start')
            stop(obj)

def startStop(obj):
    if obj['gomb1'].cget('text') == 'Start':
        start(obj)
    else:
        stop(obj)

def vege(obj):
    abl=obj['abl']
    abl.destroy()
#elesben shiftData2 nem kell(?)
def shiftDatas(obj):
    obj['labPointer']=np.roll(obj['labPointer'], -15)
    for i in range(150):
        obj['labels'][i].configure(textvariable=obj['labTextvar'][obj['labPointer'][i+15]])
    for i in range(15):
        obj['labTextvar'][obj['labPointer'][i]].set('')



