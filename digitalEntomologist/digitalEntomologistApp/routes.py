from crypt import methods
from re import L
from flask import flash, render_template, url_for, request, session, redirect
from werkzeug.wrappers import response
from digitalEntomologistApp import app
import json
import hashlib
import boto3
from boto3.dynamodb.conditions import Attr
import requests as rq

file=open("/home/attu/Desktop/ScratchNest/.credentials/awsCredentials.json")
credentialsData=json.load(file)
file.close()

dynamoDb=boto3.resource('dynamodb',
                        aws_access_key_id     = credentialsData['aws-access-key-id'],
                        aws_secret_access_key = credentialsData['aws-secret-access-key'],
                        region_name           = credentialsData['aws-region']
                                    )

userTable=dynamoDb.Table('user')  
deviceDataTable=dynamoDb.Table('deviceData')  
imageTable=dynamoDb.Table('imageKey')
jobRecordsTable = dynamoDb.Table('JobRecordsTable')



@app.route('/')
def home():
    if 'email' in session:
        response = deviceDataTable.scan(FilterExpression=Attr('email').eq(session['email']))
        # response={'Items': [{'deviceBooted': False, 'email': 'atul@gmail.com', 'serialID': 'D004', 'deviceProvisoned': True}, {'deviceBooted': True, 'email': 'atul@gmail.com', 'serialID': 'D002', 'deviceProvisoned': True}]}
        return render_template('home.html',data=response['Items'],key="Main")
    return redirect('login')

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        response = userTable.get_item(
            Key={
                'email': email
            }
        )
        if 'Item' in response:
             pas = request.form.get('password')
             pas = hashlib.md5(pas.encode()).hexdigest()
             if pas==response['Item']['password']:
                session['email']=email
                return redirect(url_for('home'))
        return render_template('login.html',msg='Wrong Credentials')
    return render_template('login.html')

@app.route('/registerUser',methods=['GET','POST'])
def registerUser():
    if request.method=='POST':
        email=request.form['email']
        name=request.form['name']
        password = request.form['password']
        password = hashlib.md5(password.encode()).hexdigest()
        #here is bug that need to be resolved in future
        #the user can re-register them-self with the same email-id forcing the password to get updated
        response=userTable.put_item(
            Item={
                'email':email,
                'name':name,
                'password':password
            }
        )
        session['email']=email
    return redirect(url_for('home'))

@app.route('/registerDevice',methods=['POST'])
def registerDevice():
    if 'email' in session and request.method=='POST':
        email=session['email']
        serialID=request.form['serialID']
        try:
            response=deviceDataTable.put_item(
                Item={
                    'serialID':serialID,
                    'email':email,
                    'deviceBooted':False,
                    'deviceProvisoned':True
                },
                ConditionExpression="attribute_not_exists(serialID)"
            )
        except Exception as e:
            flash("Device Already registered")
    return redirect(url_for('home'))
        
@app.route('/logOut')
def logout():
    session.pop('email')
    return redirect('login')

@app.route('/img')
def imgRenderer():
    resp=imageTable.scan()
    return render_template('gallery.html',data=resp['Items'])

@app.route('/getFiles',methods=['POST'])
def getFiles():
    if 'email' in session and request.method=='POST':
        serialID=request.form['serialID-query']
        date=request.form['date']
        type=request.form['File-Type']
        response = deviceDataTable.scan(FilterExpression=Attr('email').eq(session['email']))
        if 'Items' in response:
            for element in response['Items']:
                if element['serialID']==serialID:
                    resp=rq.get(f"https://e99xrdespg.execute-api.us-east-1.amazonaws.com/v1/{type}?deviceid={serialID}&date={date}")
                    resp=resp.json()
                    if type=="video":
                        return render_template('home.html',data=resp['videos'])
                    else:
                        return render_template('home.html',data=resp['files'])
            else:
                flash("This device dosen't belongs to you")
        else:
            flash("Something wrong happened")
    return redirect(url_for('home'))

@app.route('/getJobLogs')
def getJobLogs():
    if 'email' in session:
        deviceId=request.args.get("deviceId")
        response = jobRecordsTable.scan(FilterExpression=Attr('DeviceId').eq(deviceId))
        response = {"Items":response['Items']}
        # response={'Items': [{'jobId': False, 'status': 'atul@gmail.com', 'date': 'D004'}, {'jobId': True, 'status': 'atul@gmail.com', 'date': 'D002', 'deviceProvisoned': True}]}
        return response
    else:
        return {"msg":"Please Log In"}
