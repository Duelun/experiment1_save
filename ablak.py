from tkinter import *
import numpy as np
import vezerles as ve


def ablak(obj):
    abl = Tk()
    obj['abl']=abl
    abl.geometry('-50+40')
    #keret, vissz elvalasztok
    Frame(abl, height=20, width=10).grid(row=0, column=0)
    Frame(abl, height=20, width=120).grid(row=30, column=26)
    Frame(abl, height=20, width=10).grid(row=100, column=27)
    #vezerlo oszlopok
    Frame(abl, height=10, width=50).grid(row=0, column=2)
    Frame(abl, height=10, width=50).grid(row=0, column=5)
    Frame(abl, height=10, width=50).grid(row=0, column=7)
    Frame(abl, height=10, width=50).grid(row=0, column=8)
    Frame(abl, height=10, width=10).grid(row=0, column=9)
    #canvaszok felosztasa sorokra

    
    
    obj['gomb1Text']=StringVar(abl, 'Start')
    obj['gomb1']=Button(abl, textvariable=obj['gomb1Text'], command=lambda: ve.startStop(obj), width=10)
    obj['gomb1'].grid(row=1,column=1, rowspan=2, sticky=(W,N))
    obj['gomb2']=Button(abl, text='Minta',command=lambda: ve.shiftData2(obj), width=10, state='disabled')	#itt van shiftData2 tesztre
    obj['gomb2'].grid(row=3,column=1, rowspan=2, sticky=(W,N))
    obj['gomb3']=Button(abl, text='Bezar',command=lambda: ve.vege(obj),fg='red',width=10)
    obj['gomb3'].grid(row=1,column=26, sticky=(N,E))
    
    Label(abl, text='Chanel A  ').grid(row=1, column=3, rowspan=2, sticky=W)
    Label(abl, text='Chanel B  ').grid(row=3, column=3, rowspan=2, sticky=W)
    Label(abl, text='Sample number ').grid(row=5, column=3, rowspan=2, sticky=W)
    Label(abl, text='Intervall [s] ').grid(row=7, column=3, rowspan=2, sticky=W)
    obj['chA']=Entry(abl, textvariable=StringVar(abl, '1'), width=5, justify='right')
    obj['chA'].grid(row=1, column=4, rowspan=2, sticky=E)
    obj['chB']=Entry(abl, textvariable=StringVar(abl, '1'), width=5, justify='right')
    obj['chB'].grid(row=3, column=4, rowspan=2, sticky=E)
    obj['sampNum']=Entry(abl, textvariable=StringVar(abl, obj['dataNum']), width=5, justify='right')
    obj['sampNum'].grid(row=5, column=4, rowspan=2, sticky=E)
    obj['sampInt']=Entry(abl, textvariable=StringVar(abl, obj['dataNumInt']), width=5, justify='right')
    obj['sampInt'].grid(row=7, column=4, rowspan=2, sticky=E)

    obj['cButOn'] = PhotoImage(width=40, height=20)
    obj['cButOff'] = PhotoImage(width=40, height=20)
    obj['cButOn'].put(("green",), to=(0, 0, 20,20))
    obj['cButOff'].put(("red",), to=(20, 0, 39, 19))
    
    Label(abl, text='Warming   ').grid(row=1, column=6, rowspan=2, sticky=W)
    obj['cButWarm']=StringVar(obj['abl'],'0')
    obj['cBut1']=Checkbutton(obj['abl'],image=obj['cButOff'], selectimage=obj['cButOn'],variable=obj['cButWarm'],relief=RIDGE,indicatoron=False,onvalue=1,offvalue=0)
    obj['cBut1'].grid(row=1, rowspan=2, column=7, sticky=())
    obj['wt']=Entry(abl, textvariable=StringVar(abl, str(obj['warmTime'])), width=5, justify='right')
    obj['wt'].grid(row=1, column=8, sticky=E)
    obj['wti']=Entry(abl, textvariable=StringVar(abl, str(obj['warmTimeInt'])), width=5, justify='right')
    obj['wti'].grid(row=2, column=8, sticky=E)
    
    Label(abl, text='Multi read').grid(row=5, column=6, rowspan=1, sticky=W)
    obj['multiReadAct']=Label(abl, text='1', width=4, justify='right')
    obj['multiReadAct'].grid(row=5, column=7, sticky=E)
    obj['multiReadTarg']=StringVar(obj['abl'],'1')
    obj['mr']=Entry(abl, textvariable=obj['multiReadTarg'], width=5, justify='right')
    obj['mr'].grid(row=5, column=8, sticky=E)
    
    Label(obj['abl'], text='  Datas').grid(row=6, rowspan=2, column=26, sticky=W)
    obj['cButDatas']=StringVar(obj['abl'],'1')
    obj['cBut3']=Checkbutton(obj['abl'],image=obj['cButOff'], selectimage=obj['cButOn'],variable=obj['cButDatas'],relief=RIDGE,indicatoron=False,onvalue=1,offvalue=0)
    obj['cBut3'].grid(row=6, rowspan=2, column=26, sticky=(E))
    Label(abl, text='  Draw').grid(row=37, column=26, sticky=W)
    obj['cButDraw']=StringVar(obj['abl'],'1')
    obj['cBut3']=Checkbutton(obj['abl'],image=obj['cButOff'], selectimage=obj['cButOn'],variable=obj['cButDraw'],relief=RIDGE,indicatoron=False,onvalue=1,offvalue=0)
    obj['cBut3'].grid(row=37, column=26, sticky=(E))
    
    obj['can1']=Canvas(abl,bd=1,height=obj['ablakMag1'],width=obj['ablakSzel'],
                       xscrollincrement=1,yscrollincrement=1,relief=RIDGE)
    obj['can1'].grid(row=35, column=1, columnspan=24, rowspan=5, sticky=E)
    obj['can2']=Canvas(abl,bd=1,height=obj['ablakMag2'],width=obj['ablakSzel'],
                       xscrollincrement=1,yscrollincrement=1,relief=RIDGE)
    obj['can2'].grid(row=45, column=1, columnspan=24, rowspan=5, sticky=E)
    obj['can4']=Canvas(abl,bd=1,height=obj['ablakMag2'],width=obj['ablakSzel'],
                       xscrollincrement=1,yscrollincrement=1,relief=RIDGE)
    obj['can4'].grid(row=50, column=1, columnspan=24, rowspan=5, sticky=E)
    obj['can5']=Canvas(abl,bd=1,height=obj['ablakMag2'],width=obj['ablakSzel'],
                       xscrollincrement=1,yscrollincrement=1,relief=RIDGE)
    obj['can5'].grid(row=55, column=1, columnspan=24, rowspan=5, sticky=E)

    Label(abl, text='  Max A/B').grid(row=35, column=26, sticky=(N,W))
    Label(abl, text='  Min A/B').grid(row=39, column=26, sticky=(S,W))
    Label(abl, text='  Max C*').grid(row=45, column=26, sticky=(N,W))
    Label(abl, text='  Min C*').grid(row=49, column=26, sticky=(S,W))
    Label(abl, text='  Max DC*').grid(row=50, column=26, sticky=(N,W))
    Label(abl, text='  Min DC*').grid(row=54, column=26, sticky=(S,W))
    Label(abl, text='  Max Data').grid(row=55, column=26, sticky=(N,W))
    Label(abl, text='  Min Data').grid(row=59, column=26, sticky=(S,W))
    obj['can1max']=StringVar(obj['abl'],'-')
    obj['can1min']=StringVar(obj['abl'],'-')
    obj['can2max']=StringVar(obj['abl'],'-')
    obj['can2min']=StringVar(obj['abl'],'-')
    obj['can4max']=StringVar(obj['abl'],'-')
    obj['can4min']=StringVar(obj['abl'],'-')
    obj['can5max']=StringVar(obj['abl'],'-')
    obj['can5min']=StringVar(obj['abl'],'-')
    Label(abl, textvariable=obj['can1max']).grid(row=35, column=26, sticky=(N,E))
    Label(abl, textvariable=obj['can1min']).grid(row=39, column=26, sticky=(S,E))
    Label(abl, textvariable=obj['can2max']).grid(row=45, column=26, sticky=(N,E))
    Label(abl, textvariable=obj['can2min']).grid(row=49, column=26, sticky=(S,E))
    Label(abl, textvariable=obj['can4max']).grid(row=50, column=26, sticky=(N,E))
    Label(abl, textvariable=obj['can4min']).grid(row=54, column=26, sticky=(S,E))
    Label(abl, textvariable=obj['can5max']).grid(row=55, column=26, sticky=(N,E))
    Label(abl, textvariable=obj['can5min']).grid(row=59, column=26, sticky=(S,E))
    obj['T1']=Entry(abl, textvariable=StringVar(abl, 'C* A1'), width=10, justify='right')
    obj['T1'].grid(row=51, column=26, rowspan=1, sticky=())
    obj['T2']=Entry(abl, textvariable=StringVar(abl, 'C* B1'), width=10, justify='right')
    obj['T2'].grid(row=52, column=26, rowspan=1, sticky=())
    obj['T3']=Entry(abl, textvariable=StringVar(abl, ''), width=10, justify='right')
    obj['T3'].grid(row=46, column=26, rowspan=1, sticky=())
    obj['T4']=Entry(abl, textvariable=StringVar(abl, ''), width=10, justify='right')
    obj['T4'].grid(row=47, column=26, rowspan=1, sticky=())

#tabla
    for osz, ert in enumerate(obj['dtData']['name']):
        osz=osz+10
        Label(abl, text=ert).grid(row=1, column=osz, sticky=())
    for i in range(1,7):
        obj['fejlectext'+str(i)]=StringVar(obj['abl'],'')
        obj['fejlec'+str(i)]=Label(obj['abl'], textvariable=obj['fejlectext'+str(i)])
        obj['fejlec'+str(i)].grid(row=1, column=i+13, sticky=())
    for i, e in enumerate(obj['dtCalc']['name'][2:]):
        obj['fejlec2'+str(i)]=Label(obj['abl'], text=e)
        obj['fejlec2'+str(i)].grid(row=1, column=i+21, sticky=())
        if i > 0:
            obj['fejlec2'+str(i)].config(fg=obj['dataColor']['1'][e])
    
    obj['labels']=[]
    obj['labPointer']=np.arange(165)
    obj['labTextvar']=[]
    for i in range(165):
        obj['labTextvar'].append(StringVar(obj['abl'],'-'))
    szel=[4,18,14,14,5,5,5,5,5,5,1,5,9,9,8]*11
    i=0
    for sor in range(10):
        dataSor = sor+2
        for osz in range(15):
            dataOsz = osz+10
            obj['labels'].append(Label(abl, textvariable=obj['labTextvar'][obj['labPointer'][i+15]], width=szel[osz], height=1, relief=RIDGE))
            obj['labels'][i].grid(row=dataSor, column=dataOsz, sticky=())
            i+=1
    
    



