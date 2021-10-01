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
                if a in allDict[k]["job"]:
                    neededDict[k]=allDict[k]["job"]
                    break
        return dict_add([neededDict[k] for k in neededDict])

def dict_add(dicts):
    d={}
    for d1 in dicts:
        for item in d1:
            if item in d:
                d[item]+=d1[item]
            else:
                d[item]=d1[item]
    return d
def dict_eval(dict1,*keys):
    nm=1000
    for k in keys:
        if not k in dict1:
            continue
        one_dict=dict1[k]
        val = one_dict[k]
        for k1 in one_dict:
            one_dict[k1]=int(nm*one_dict[k1]/val/len(keys))/nm
        del one_dict[k]
        dict1[k] = one_dict
    dict1 = dict_add([dict1[k] for k in keys if k in dict1])
    return Counter(dict1).most_common(10)
def recommend(*keys):
    return dict(dict_eval(init(keys),*keys))