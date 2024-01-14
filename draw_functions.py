import numpy as np
import time as ti


def canvasPreset(obj):
    #obj['pixelDraw']
    lp = 30
    rp = 30
    yph1 = 10
    ypl1 = 10
    yph2 = 5
    ypl2 = 5
    yph4 = 5
    ypl4 = 5
    yph5 = 5
    ypl5 = 5
    c1 = {'ablakMag':obj['ablakMag1']-yph1-ypl1, 'yPix':(obj['ablakMag1']-yph1-ypl1)/2, 'y0':0, 'y1':0,
          'pos':lp,'yPadH':yph1, 'yPadL':ypl1,
          'firstLive':2, 'canvas': obj['can1'], 'labmin':obj['can1min'], 'labmax':obj['can1max']}
    c2 = {'ablakMag':obj['ablakMag2']-yph2-ypl2, 'yPix':(obj['ablakMag2']-yph2-ypl2)/2, 'y0':0, 'y1':0,
          'pos':lp,'yPadH':yph2, 'yPadL':ypl2,
          'firstLive':1,'canvas': obj['can2'], 'labmin':obj['can2min'], 'labmax':obj['can2max']}
    c4 = {'ablakMag':obj['ablakMag4']-yph4-ypl4, 'yPix':(obj['ablakMag4']-yph4-ypl4)/2, 'y0':0, 'y1':0,
          'pos':lp,'yPadH':yph4, 'yPadL':ypl4,
          'firstLive':1, 'canvas': obj['can4'], 'labmin':obj['can4min'], 'labmax':obj['can4max']}
    c5 = {'ablakMag':obj['ablakMag5']-yph5-ypl5, 'yPix':(obj['ablakMag5']-yph5-ypl5)/2, 'y0':0, 'y1':0,
          'pos':lp,'yPadH':yph5, 'yPadL':ypl5,
          'firstLive':2, 'canvas': obj['can5'], 'labmin':obj['can5min'], 'labmax':obj['can5max']}
    obj['canvas']={'regionX':obj['ablakSzel']-rp, 'scrollReg':obj['ablakSzel'],
                   'leftPad':lp, 'rightPad':rp, '1':c1, '2':c2, '4':c4, '5':c5}    
    
    if obj['gomb1'].cget('text') == 'StopWarm' or obj['gomb1'].cget('text') == 'StopReadWarm':
        a = (float(obj['wt'].get()) // float(obj['wti'].get())) * obj['pixelDraw'] + lp + rp
    else:
        a = float(obj['sampNum'].get()) * obj['pixelDraw'] + lp + rp

    obj['canvas']['1']['pos']=obj['canvas']['1']['pos']-obj['pixelDraw']
    obj['canvas']['2']['pos']=obj['canvas']['2']['pos']-obj['pixelDraw']
    obj['canvas']['4']['pos']=obj['canvas']['4']['pos']-obj['pixelDraw']
    obj['canvas']['5']['pos']=obj['canvas']['5']['pos']-obj['pixelDraw']
    if a > obj['ablakSzel']:
        obj['canvas']['scrollReg'] = a
    obj['can1'].configure(scrollregion = ("0 -"+str(obj['ablakMag1'])+" "+str(obj['canvas']['scrollReg'])+" 0"))
    obj['can2'].configure(scrollregion = ("0 -"+str(obj['ablakMag2'])+" "+str(obj['canvas']['scrollReg'])+" 0"))
    obj['can4'].configure(scrollregion = ("0 -"+str(obj['ablakMag4'])+" "+str(obj['canvas']['scrollReg'])+" 0"))
    obj['can5'].configure(scrollregion = ("0 -"+str(obj['ablakMag5'])+" "+str(obj['canvas']['scrollReg'])+" 0"))
    obj['can1'].xview('moveto', '0')
    obj['can2'].xview('moveto', '0')
    obj['can4'].xview('moveto', '0')
    obj['can5'].xview('moveto', '0')
    
    obj['drawLastPoint'] = {'1':{},'2':{}, '4':{}, '5':{}}
def shiftX(obj, c):
    obj['canvas'][c]['pos'] = obj['canvas'][c]['pos'] + obj['pixelDraw']
    if obj['canvas'][c]['pos'] > obj['canvas']['regionX']:
        obj['canvas']['regionX'] = obj['canvas']['regionX'] + obj['pixelDraw']
        obj['can1'].xview('scroll', obj['pixelDraw'], 'unit')
        obj['can2'].xview('scroll', obj['pixelDraw'], 'unit')
        obj['can4'].xview('scroll', obj['pixelDraw'], 'unit')
        obj['can5'].xview('scroll', obj['pixelDraw'], 'unit')
def limes(obj, d, datas, c, group):
    l = datas[0]
    h = datas[0]
    for e in datas:
        l = min(l,e)
        h = max(h,e)
    
    if d[0] == obj['canvas'][c]['firstLive']:
        obj['canvas'][c]['y0'] = l
        obj['canvas'][c]['labmin'].set(str("{:.3f}".format(l)))
        obj['canvas'][c]['y1'] = h
        obj['canvas'][c]['labmax'].set(str("{:.3f}".format(h)))
        dif = obj['canvas'][c]['y1'] - obj['canvas'][c]['y0']
        if dif==0:
            dif = 2
        obj['canvas'][c]['yPix'] = obj['canvas'][c]['ablakMag'] / dif
    else:
        if l < obj['canvas'][c]['y0']:
            lim = obj['canvas'][c]['ablakMag'] + obj['canvas'][c]['yPadL']
            if obj['canvas'][c]['y1'] != obj['canvas'][c]['y0']:
                rate = (obj['canvas'][c]['y1'] - obj['canvas'][c]['y0']) / (obj['canvas'][c]['y1'] - l)
                for e in obj['drawLastPoint'][c]:
                    obj['drawLastPoint'][c][e] = lim - (lim - obj['drawLastPoint'][c][e]) * rate 
            else:
                rate =  obj['canvas'][c]['yPadH'] / (obj['canvas'][c]['yPix'] + obj['canvas'][c]['yPadH'])
                for e in obj['drawLastPoint'][c]:
                    obj['drawLastPoint'][c][e] = lim
                lim = obj['canvas'][c]['ablakMag'] + obj['canvas'][c]['yPadL'] + obj['canvas'][c]['yPadH']
            obj['canvas'][c]['canvas'].scale(group, 0, -lim, 1, rate)
            obj['canvas'][c]['y0'] = l
            obj['canvas'][c]['labmin'].set(str("{:.3f}".format(l)))
            dif = obj['canvas'][c]['y1'] - obj['canvas'][c]['y0']
            obj['canvas'][c]['yPix'] = obj['canvas'][c]['ablakMag'] / dif
    
        if h > obj['canvas'][c]['y1']:
            lim = obj['canvas'][c]['yPadL']
            if obj['canvas'][c]['y1'] != obj['canvas'][c]['y0']:
                rate = (obj['canvas'][c]['y1'] - obj['canvas'][c]['y0']) / (h - obj['canvas'][c]['y0'])
                for e in obj['drawLastPoint'][c]:
                    obj['drawLastPoint'][c][e] = lim + (obj['drawLastPoint'][c][e] - lim) * rate 
            else:
                rate = obj['canvas'][c]['yPadL'] / (obj['canvas'][c]['yPix'] + obj['canvas'][c]['yPadL'])
                for e in obj['drawLastPoint'][c]:
                    obj['drawLastPoint'][c][e] = lim
                lim = 0
            obj['canvas'][c]['canvas'].scale(group, 0, -lim, 1, rate)
            obj['canvas'][c]['y1'] = h
            obj['canvas'][c]['labmax'].set(str("{:.3f}".format(h)))
            dif = obj['canvas'][c]['y1'] - obj['canvas'][c]['y0']
            obj['canvas'][c]['yPix'] = obj['canvas'][c]['ablakMag'] / dif
    
def draw(obj, d, datas, name, c, group='all'):
    al = len(datas)
    if al == 0:
        return
    shiftX(obj, c)
    if obj['canvas'][c]['firstLive'] > d[0]:
        return
    limes(obj, d, datas, c, group)
    
    for i, e in enumerate(name):
        if obj['canvas'][c]['y1'] != obj['canvas'][c]['y0']:
            y = (datas[i] - obj['canvas'][c]['y0']) * obj['canvas'][c]['yPix'] + obj['canvas'][c]['yPadL']
        else:
            y = obj['canvas'][c]['yPix'] + obj['canvas'][c]['yPadL']
        if e not in obj['drawLastPoint'][c]:
            obj['drawLastPoint'][c][e] = y
        if c=='4':
            e1 = '1'
        else:
            e1 = e
        obj['canvas'][c]['canvas'].create_line(obj['canvas'][c]['pos'] - obj['pixelDraw'],
                                               -obj['drawLastPoint'][c][e],
                                               obj['canvas'][c]['pos'],
                                               -y,
                                               width=1, fill=obj['dataColor'][c][e1], tags= (e, 'graf'))
        obj['drawLastPoint'][c][e] = y
    
def drawBar(obj, d, datas, name, c, group='all'):
    al = len(datas)
    if al == 0:
        return
    
    shiftX(obj, c)
    if obj['canvas'][c]['firstLive'] > d[0]:
        return
    
    limes(obj, d, datas, c, group)
    y0 = (0 - obj['canvas'][c]['y0']) * obj['canvas'][c]['yPix'] + obj['canvas'][c]['yPadL']
    if obj['canvas'][c]['firstLive'] == d[0]:
        obj['canvas'][c]['canvas'].create_line(0,
                                                -y0,
                                                obj['canvas']['scrollReg'],
                                                -y0,
                                                width=1, fill='black', tags= ('nullkor'))
    

    for i, e in enumerate(name):
        y1 = (datas[i] - obj['canvas'][c]['y0']) * obj['canvas'][c]['yPix'] + obj['canvas'][c]['yPadL']
        obj['canvas'][c]['canvas'].create_line(obj['canvas'][c]['pos']+i,
                                                -y0,
                                                obj['canvas'][c]['pos']+i,
                                                -y1,
                                                width=1, fill=obj['dataColor'][c][e], tags= (e, 'bar'))
    
#########
def clearAblak(obj):
    #tomboket torli
    #shedulokat torli
    #rajzokat torli
    #szinkodot torli
    for i in range(165):
        obj['labTextvar'][i].set('')
    
    obj['can1'].delete("all")
    obj['can2'].delete("all")
    obj['can4'].delete("all")
    obj['can5'].delete("all")
    obj['can1max'].set('-')
    obj['can1min'].set('-')
    obj['can2max'].set('-')
    obj['can2min'].set('-')
    obj['can4max'].set('-')
    obj['can4min'].set('-')
    obj['can5max'].set('-')
    obj['can5min'].set('-')

