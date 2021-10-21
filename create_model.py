import numpy as np
import tensorflow as tf
import json
#CREATE_MODEL
divideNum=25
base_learning_rate = .001
def create_model(input_num,train=False):
  model = tf.keras.Sequential()
  model.add(tf.keras.layers.Dense(input_num, input_shape=(input_num,)))
  if train:
    model.add(tf.keras.layers.Dense(1))
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
            loss="mse",
            metrics=['accuracy'])
  else:
    model.add(tf.keras.layers.Dense(1,activation="relu"))
  return model

def getLables():
  unique_numbers=[]
  with open('./files/expense_data.txt') as json_file:
    allDict = json.load(json_file)
    for k in allDict:
      unique_numbers.extend(allDict[k]['job'].keys())
  unique_numbers = list(set(unique_numbers)) 
  for i in range(len(unique_numbers)):
    unique_numbers[i] = int(unique_numbers[i])//divideNum
  unique_numbers = list(set(unique_numbers))
  unique_numbers.sort()
  labels2 = unique_numbers + ["totalItems","sumItems","time"]
  return labels2
def dict_to_row(item,labels):
  x = np.zeros(len(labels)-1)
  count_found = []
  for key in item:
    if not str(key).isnumeric():
        continue
    pos = labels.index(int(key)//divideNum) if int(key)//divideNum in labels else -5
    if pos == -5 :
        continue
    count_found.append(key)
    x[pos] += item[key]
    x[-3] +=1
    x[-2] +=item[key]
  return x,count_found
def run():
  labels = getLables()
  with open('./files/expense_data.txt') as json_file:
    allDict = json.load(json_file)
    x = np.zeros((len(allDict),len(labels)))
    for i,key in enumerate(allDict):
      item = allDict[key]['job']
      _x,_ = dict_to_row(item,labels)
      x[i]=[*_x,allDict[key]['time']]
    
    train_dataset = tf.data.Dataset.from_tensor_slices((x[:,:-1], x[:,-1]))
    dataset =train_dataset.batch(100).shuffle(len(x))

    # vals = np.array([x[i,:] for i in np.random.choice(len(x),int(len(x)*.8))])
    # val_dataset = tf.data.Dataset.from_tensor_slices((vals[:,:-1], vals[:,-1]))
    # dataset = val_dataset.batch(100).shuffle(len(vals))

    input_len = len(labels)-1
    
    try:
      model = create_model(input_len,train=True)
      model.load_weights("./m1checkpoints/point")
      model.fit(dataset, epochs=60,verbose=0)
    except:
      model = create_model(input_len,train=True)
      model.fit(dataset, epochs=60,verbose=0)
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate/100),
                    loss='mse',
                    metrics=['accuracy'])
    model.fit(dataset, epochs=80,verbose=0)

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate/5000),
                    loss='mse',
                    metrics=['accuracy'])
    model.fit(dataset, epochs=80,verbose=0)

    model.save_weights('./m1checkpoints/point')
if __name__ == "__main__":
  run()
