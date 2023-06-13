#!/usr/bin/env python
import os
import io
import json

from flask import Flask
from flask import request
from pymongo import MongoClient

from flask_restful import Resource, Api
import pandas as pd
from s3_handler import S3Handler


app = Flask(__name__)
api = Api(app)

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient("mongo:27017")

db = client.data_model    #Select the database
tenants = db.tenant #Select the collection


class UploadCSV(Resource):
    def post(self):
        if "file" not in request.files:
            return "No user_file key in request.files"
        file_ = request.files['file']
        if file_.filename == "":
            return "Please select a file"
        print(file_.filename, "file_.filename")
        s3_handler = S3Handler()
        s3_handler.upload_file_to_s3(file_)
        data = pd.read_csv(file_)
        data_dict = data.to_dict()
        self.insert_model()
        return json.dumps(data_dict)

    def insert_model(delf, data_dict):
        tenants.insert_one({"tenant": tenant, "data": data_dict})


api.add_resource(UploadCSV, '/v1/upload')
    

@app.route("/list")
def lists ():
    #Display the all Tasks
    tenants_list = tenants.find()
    a1="active"
    return render_template('index.html',a1=a1,tenants=tenants_list, t=title, h=heading)    


@app.route("/action", methods=['POST'])
def action ():
    #Adding a Task
    name = request.values.get("name")
    desc = request.values.get("desc")
    date = request.values.get("date")
    pr = request.values.get("pr")
    tenants.insert_one({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
    return redirect("/list")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get("FLASK_SERVER_PORT", 9090), debug=True)
