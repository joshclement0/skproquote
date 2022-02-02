import pandas as pd
from collections import Counter
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def create(outlier = False,p_val = .9,graph_limit = 500):
    prename = "files/"
    name2 = "fullGraph0.png"
    name1 = "halfGraph0.png"
    name3 = "halfGraph1.png"
    name4 = "halfGraph2.png"

    full_df = pd.read_csv("./files/results.csv")
    
    res_df = full_df
    color = "b."
    res_df = res_df[res_df.pNFound>p_val]
    pretitle = "%.2f"%(p_val)+" in Model -"
    y_hat = res_df.guess
    y_tru = res_df.real
    vals = y_tru-y_hat
    x = y_tru
    y = y_hat
    plt.plot(x,x,'g:',markersize=1,label='optimal')
    plt.plot(x,y,'ro',markersize=2,label='Actual Data')
    plt.xlabel("Real Hours")
    plt.ylabel("Guess Hours")
    plt.xlim(-5,graph_limit)
    plt.ylim(-5,graph_limit)
    plt.legend()
    plt.title('Real vs Guess')
    plt.savefig(prename+name1)
    plt.clf()

    factor = 100
    c=Counter([int(a*factor)/factor for a in vals]) 
    c_true = Counter(x)
    c_gues = Counter(y)
    if outlier:
        x = [x for x in c if c[x]>1]
        x_true = [i for i in c_true if c_true[i]>1]
        x_gues = [i for i in c_gues if c_gues[i]>1]
    else:
        x = [x for x in c]
        x_true = [i for i in c_true]
        x_gues = [i for i in c_gues]
    y = [c[_x] for _x in x]
    y_true = [c_true[_x] for _x in x_true]
    y_gues = [c_gues[_x] for _x in x_gues]

    std = np.std([x[i] for i in range(len(x)) for j in range(y[i])])
    avg = np.dot(x,y)/sum(y)
    plt.plot(x,y,color,markersize=2)
    plt.xlim(-graph_limit/2,graph_limit/2)
    plt.xlabel("Actual - Model Guess")
    plt.ylabel("Count")
    plt.title('Bell Curve - Mean: '+"%.2f"%avg+' Std: '+"%.2f"%std)
    plt.savefig(prename+name2)
    plt.clf()

    std_true = np.std(y_tru)
    std_gues = np.std(y_hat)
    avg_true = sum(y_tru)/len(y_tru)
    avg_gues = sum(y_hat)/len(y_hat)

    plt.plot(x_true,y_true,'go',markersize=2,label='Actual Data - Mean: {:.2f} Std: {:.2f}'.format(avg_true,std_true))
    plt.plot(x_gues,y_gues,'bo',markersize=2,label='Model Data - Mean: {:.2f} Std: {:.2f}'.format(avg_gues,std_gues))
    plt.xlim(0,graph_limit/2)
    plt.xlabel("Time")
    plt.ylabel("Count")
    plt.title("Summary of Time sampled")
    plt.legend()
    plt.savefig(prename+name4)
    plt.clf()

    x_1 = y_tru.unique().tolist()
    x_1.sort()
    y_tru_list = y_tru.tolist()
    y_all = [[] for i in range(len(x_1))]
    for a,guess_x in enumerate(y_hat):
      ind = x_1.index(y_tru_list[a])
      y_all[ind].append(guess_x)
    y_final = []
    y_std = []
    y_std_below=[]
    for a,guesses in enumerate(y_all):
      avg = sum(guesses)/len(guesses)
      y_final.append(avg)
      st = np.std(guesses)
      y_std.append(st+avg)
      y_std_below.append(avg-st)
    plt.plot(x_1,x_1,'g:',markersize=1,label='optimal')
    plt.plot(x_1,y_std,'bo',markersize=1,label='std')
    plt.plot(x_1,y_std_below,'bo',markersize=1)
    plt.plot(x_1,y_final,'ro',markersize=2,label='average')
    plt.xlim(-5,graph_limit)
    plt.ylim(-5,graph_limit)
    plt.xlabel("Actual Result")
    plt.ylabel("Average Guess")
    plt.legend()
    plt.savefig(prename+name3)
    plt.clf()

    return name1,name2,name3,name4
if __name__ == "__main__":
    create(outlier = True,p_val = .9,graph_limit = 200)