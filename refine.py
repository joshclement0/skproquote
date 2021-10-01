import json
import pandas as pd
import create_model
expensefile = './files/expense_data.txt'
def run():
  labels = create_model.getLables()
  wrongkeys = []
  allDict={}
  with open(expensefile) as json_file:
    allDict = json.load(json_file)
    for key in allDict:
      item = allDict[key]['job']
      _,pFound = create_model.dict_to_row(item,labels)
      if len(pFound) != len(item):
        wrongkeys.append(key)
    for k in wrongkeys:
      del allDict[k]
  with open(expensefile,'w') as json_file:
    json.dump(allDict, json_file)

def add(jobID,item):
  if not (item['time'] and item['job']) or not jobID or jobID == "NONE":
    raise Exception("incorrect parameters")
  allDict = {}
  with open(expensefile) as json_file:
    allDict = json.load(json_file)
    if allDict[jobID]:
      raise Exception("JobID already found")
    allDict[jobID] = item
  with open(expensefile,'w') as json_file:
    json.dump(allDict, json_file)
def addCSV(new_csv):
  df = pd.read_csv(new_csv)
  item_df = df
  for art in ["LH","KMT"]:
    item_df = item_df[item_df.priceUnit != art]
  jobIDs = item_df.jobId.unique()
  time_df = df[df.priceUnit == "LH"]

  for j in jobIDs:
    _itemdf = item_df[item_df.jobId == j]
    _timedf = time_df[time_df.jobId == j]
    data ={}
    for row in _itemdf.iterrows():
      if row[1].articleNumber in data:
        data[row[1].articleNumber] += int(row[1].quantity)
      else:
        data[row[1].articleNumber] = int(row[1].quantity)
    time = int(sum(_timedf.quantity))
    try:
      add(str(j),{"job":data,"time":time,"jobID":str(j)})
    except:
      pass
  
if __name__ == '__main__':
  run()