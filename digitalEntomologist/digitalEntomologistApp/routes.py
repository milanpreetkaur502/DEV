from re import L
from flask import flash, render_template, url_for, request, session, redirect
from werkzeug.wrappers import response
from digitalEntomologistApp import app
import json
import hashlib
import boto3
from boto3.dynamodb.conditions import Attr

file=open("/home/attu/Desktop/ScratchNest/awsCredentials.json")
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


@app.route('/')
def home():
    if 'email' in session:
        response = deviceDataTable.scan(FilterExpression=Attr('email').eq(session['email']))
        # response={'Items': [{'deviceBooted': False, 'email': 'atul@gmail.com', 'serialID': 'D004', 'deviceProvisoned': True}, {'deviceBooted': True, 'email': 'atul@gmail.com', 'serialID': 'D002', 'deviceProvisoned': True}]}
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