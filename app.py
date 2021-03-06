import numpy as np
import flask
from flask import request, render_template, send_file

import pandas as pd

import os

import create_model
import refine
import recomender
import create_img

#enabling GPU increases the speed

app = flask.Flask(__name__)

labels= create_model.getLables()


model1=0
def load_models():
    global model1
    model1 = create_model.create_model(len(labels)-1)
    model1.load_weights("./m1checkpoints/point")


@app.route('/',methods=["GET"])
def formHome():
    return render_template("readme.html")

@app.route('/images',methods=['GET'])
def getImg():
    filename = request.args.get("img")
    return send_file("./files/"+filename)

@app.route('/results/csv',methods=['GET'])
def allcsv():
    return send_file("./files/results.csv")
@app.route('/results/reset')
def reset():
    fields = ["jobID","real","guess",'guess2',"pNFound","pNFound2"]
    with open("./files/results.csv","w") as csv:
        csv.write(",".join([str(f) for f in fields]))
@app.route('/results', methods=['GET'])
def home():
    outlier = request.args.get("out")
    try:
        p_val = request.args.get("p")
        p_val = float(p_val)
    except:
        p_val = .9
    try:
        graph_limit = request.args.get("size")
        graph_limit = int(graph_limit)
    except:
        graph_limit = 200
    name1,name2,name3,name4 = create_img.create(outlier,p_val,graph_limit)
    return render_template("home.html",main_img1 = "/images?img="+name1,alt_img1="/images?img="+name3,alt_img2="/images?img="+name2,alt_img3="/images?img="+name4)

@app.route('/api/add',methods=["GET"])
def form():
    return render_template("upload.html",extra="")

@app.route('/api/addCSV',methods=["POST"])
def addToFile():
    try:
        csv = request.files['csv']
        if not csv:
            raise Exception("FILE NOT FOUND")
        refine.addCSV(csv)
        refine.run()
        create_model.run()
        return "SUCCESS",200
    except Exception as e:
        return render_template("upload.html",extra = "<p>Error Occured<br>{}</p>".format(e)),400
    
@app.route("/api/retrain")
def retrain():
    try:
        refine.run()
        create_model.run()
        return "success",201
    except Exception as e:
        return "{}".format(e),500


@app.route('/api/predict',methods=["POST"])
def predict():
    form = request.get_json()
    try:
        item = form.get("job")
        if item != item and type(item) is not dict:
            raise Exception("job must be a dictionary")
    except Exception as e :
        return str(e),400
    try:
        jobID = form.get("jobID")
        if jobID != jobID:
            raise Exception("empty")
    except:
        jobID = "NONE"

    try:
        # return form,200
        x,p_found = create_model.dict_to_row(item,labels)
        y_hat2 = model1.predict(x.reshape(1,len(x)))
        y_hat2 = ["%.2f"%y_h for y_h in y_hat2[0]]
        try:
            time = form.get("time")
            fields = [jobID,time,*y_hat2,"%.2f"%(len(p_found)/len(item))]
            with open('./files/results.csv', 'a') as f:
                f.write("\n"+",".join([str(fi) for fi in fields]))
            refine.add(jobID,form)
        except:
            pass
        return {"guess":y_hat2,"found":p_found}
    except Exception as e:
        return str(e),500
@app.route('/api/test',methods=["GET"])
def test():
    return render_template("test.html")

@app.route('/api/recommend',methods=["GET"])
def rec():
    articleList = request.args.getlist("nums")
    articleNums = []
    if articleList != articleList:
        return "unavailiable Parameters", 400
    for i in articleList:
        if not i.isnumeric() or len(i)!=7:
            return "Parameters must contain only valid numeric articles",400
        articleNums.append(int(i))
    return recomender.recommend(*articleNums)
if __name__ == '__main__':
    load_models()
    port = int(os.environ.get('PORT', 5005))
    from waitress import serve
    serve(app, host="0.0.0.0", port=port)
    # app.run(host='0.0.0.0',port=port)
