# pronto-time-estimator

-Time Estimator
send a dictionary with key "job", and opptionally "jobID","time". "job" will contain a dictionary with pairs of articleNum:quantity
curl -i -X POST -H "Content-Type: application/json" -d "{\\\"job\\\":{\\\"5062806\\\":\\\"2\\\",\\\"9310331\\\":\\\"1\\\",\\\"5066603\\\":\\\"2\\\",\\\"3401437\\\":\\\"1\\\",\\\"5020436\\\":\\\"1\\\"},\\\"jobID\\\":\\\"832345\\\"}" localhost:5000/api/predict

you can also use the browser tool at localhost:5000/api/test

-Recommender
send the list of article numbers currently in the job as url parameters
curl -G localhost:5000/api/recommend -d 'nums=6023039&nums=5020145'

Because of its large size, the models have not been saved, there are multiple options to remedie that problem.
    1. the dockerfile includes a command to train the models ("RUN python create_model.py" nothing needs to be done)
    2. run the file create_model from the command line with
        python create_model.py 
        You will have to remove the command to run from the dockerfile
Data to be trained will be added automatically if a jobID and time is sent to the prediction url, but can also be added either through localhost:5000/api/add in the browser or by sending a csv to localhost:5000/api/addCSV, the models will automatically be retrained. The models can be retrained at any time through localhost:5000/api/retrain

Each time a prediction is made with an attached time, it is updated to the results csv. You can either view the results by downloading the file through localhost:5000/results/csv, or by viewing some amazing charts at localhost:5000/results. To clear this table at any time send a get request to localhost:5000/results/reset
For viewing charts options include localhost:5000/results?p=.1&out=true. 'p' is the percent of articles found in the model, whereas 'out' removes all single occurences (outliers). NOTE: if out=False is the desired outcome, leave it out

NOTES:
This uses a model combining close ETIM article numbers, the ranges are defined in the file matrix.csv. Better results were achieved by not combining article numbers, but this increased the size as well as the time needed for training. I have tried adding more layers/nodes, but the increases (if any) didn't seem worth the cost. KNNRegression was also attempted but didn't improve accuracy and didn't seem as relevent. 