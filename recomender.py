import numpy as np
from collections import Counter
import pandas as pd
import json

##use with recomender.recommend( *[ articleNum1, articleNum2, articleNum3 ] )
##      or recomender.recommend( articleNum1, articleNum2, articleNum3 )
def init(articlenums):
    with open('./files/expense_data.txt') as json_file:
        allDict = json.load(json_file)
        neededDict = {}
        for k in allDict:
            for a in articlenums:
                if str(a) in allDict[k]["job"]:
                    neededDict[k]=allDict[k]["job"]
                    break
        return dict_add([neededDict[k] for k in neededDict])

def dict_add(dicts):
    d={}
    for d1 in dicts:
        for item in d1:
            if item in d:
                d[item]+=d1[item]
                # d[item]+=1
            else:
                d[item]=d1[item]
                # d[item]=1
    return d
def dict_eval(dict1,keys):
    nm=1000
    val=0
    length=0
    for k in keys:
        if not str(k) in dict1:
            continue
        val += dict1[k]
        length+=1
        del dict1[k]
    if length ==0:
      raise Exception("No Keys found")
    val = val/length
    retDict = {}
    for k,v in sorted(dict1.items(),key=lambda item: item[1]):
      retDict[k]= v/val
      if len(retDict)>9:
        break
    return retDict
def recommend(*keys):
    return dict(dict_eval(init(keys),[str(k)for k in keys]))
