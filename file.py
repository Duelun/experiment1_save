from os import getcwd
from time import strftime
import numpy as np


def save(obj):
    startTime = strftime('%y%m%d'+'-'+'%H%M%S',obj['startTime'])
    obj['fileName'] = getcwd() + '/adatok/' + startTime + '#'+str(obj['sampInt'].get())+'+0' + '.raw'
    f = open(obj['fileName'],'w')
    
    data = '0;'+startTime+';Ch(1);Ch(1);'+str(obj['sampInt'].get())+';0;None'+'\n'
    f.write(data)
    dataName = '1;'
    dataForm = '2;'
    name = obj['dataReaded'].dtype.names
    for e in name:
        if np.issubdtype(obj['dataReaded'].dtype[e], np.integer):
            dataForm += 'int'+';'
        else:
            dataForm += 'float'+';'
        if e == 'Time' or e == 'Num':
            e += 'D'
        if ' ' in e:
            eL = e.split(' ')
            e = eL[0] + eL[1]
        dataName += str(e) + ';'
    name = obj['thermReaded'].dtype.names
    for e in name:
        if np.issubdtype(obj['thermReaded'].dtype[e], np.integer):
            dataForm += 'int'+';'
        else:
            dataForm += 'float'+';'
        if e == 'Time' or e == 'Num':
            e += 'T'
        if ' ' in e:
            eL = e.split(' ')
            e = eL[0] + eL[1]
        dataName += str(e) + ';'
    dataName = dataName[:len(dataName)-1]
    dataName += '\n'
    dataForm = dataForm[:len(dataForm)-1]
    dataForm += '\n'
    f.write(dataName)
    f.write(dataForm)
    
    dataList = {}
    for i, e in enumerate(obj['dataReaded']):
        dataList[str(i)] = ''
        for d in e:
            dataList[str(i)] += str(d) + ';'
        if i == obj['recordNum']['data']:
            break
    for i, e in enumerate(obj['thermReaded']):
        if str(i) not in dataList:
            dataList[str(i)] = ''
        for d in e:
            dataList[str(i)] += str(d) + ';'
        if i == obj['recordNum']['therm']:
            break
    for i in dataList:
        e = '3;' + dataList[i]
        e = e[:len(e)-1] + '\n'
        f.write(e)
    
    f.close()


