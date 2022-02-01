from re import L
from flask import render_template, url_for, request, session, redirect
from werkzeug.wrappers import response
from digitalEntomologistApp import app
import json
import boto3
from boto3.dynamodb.conditions import Attr

file=open("/home/attu/Desktop/ScratchNest/awsCredentials.json")
credentialsData=json.load(file)

dynamoDb=boto3.resource('dynamodb',
                        aws_access_key_id     = credentialsData['aws-access-key-id'],
                        aws_secret_access_key = credentialsData['aws-secret-access-key'],
                        region_name           = credentialsData['aws-region']
                                    )

userTable=dynamoDb.Table('user')  
deviceDataTable=dynamoDb.Table('deviceData')  
imageTable=dynamoDb.Table('imageKey')




@app.route('/')
def home():
    if 'email' in session:
        response = deviceDataTable.scan(FilterExpression=Attr('email').eq(session['email']))
        # response={'Items': [{'deivceBooted': 'true', 'email': 'atul@gmail.com', 'serialID': 'D004', 'deviceProvisoned': True}, {'deivceBooted': 'true', 'email': 'atul@gmail.com', 'serialID': 'D002', 'deviceProvisoned': True}]}
        return render_template('home.html',data=response['Items'])
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
        if 'Item' in response and request.form.get('password')==response['Item']['password']:
            session['email']=email
            return redirect(url_for('home'))
        return render_template('login.html',msg='Wrong Credentials')
    return render_template('login.html')

@app.route('/registerUser',methods=['GET','POST'])
def registerUser():
    if request.method=='POST':
        email=request.form['email']
        name=request.form['name']
        password=request.form['password']
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
        response=deviceDataTable.put_item(
            Item={
                'serialID':serialID,
                'email':email,
                'deivceBooted':False,
                'deviceProvisoned':True
            }
        )
    return redirect(url_for('home'))
        
@app.route('/logOut')
def logout():
    session.pop('email')
    return redirect('login')

@app.route('/img')
def imgRenderer():
    resp=imageTable.scan()
    return render_template('gallery.html',data=resp['Items'])