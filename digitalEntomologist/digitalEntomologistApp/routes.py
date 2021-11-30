from re import L
from flask import render_template, url_for, request, session, redirect
from digitalEntomologistApp import app
import boto3
from boto3.dynamodb.conditions import Key


userTable=dynamoDb.Table('user')  
deviceDataTable=dynamoDb.Table('deviceData')  



@app.route('/')
def home():
    if 'email' in session:
        # response = deviceDataTable.query(
        # KeyConditionExpression=Key('email').eq(session['email'])
        # )
        # print(response)
        return render_template('home.html')
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
                'deviceProvisoned':False
            }
        )
    return redirect(url_for('home'))
        
@app.route('/logOut')
def logout():
    session.pop('email')
    return redirect('login')
