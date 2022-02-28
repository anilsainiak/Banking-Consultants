from flask import Flask,render_template,request,redirect,url_for
from flask_mail import Mail,Message
import numpy as np
import pickle
import pandas as pd
import smtplib


app = Flask(__name__, template_folder='templates')
model=pickle.load(open('static/bank_lr.pkl','rb'))
mail=Mail(app)

income=0
lon=0





@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/gym')
def gym():
    return render_template('gym.html')

@app.route('/loan')
def loan():
    return render_template('details.html')

@app.route('/si')
def si():
    return render_template('si.html')

@app.route('/ci')
def ci():
    return render_template('ci.html')

@app.route('/details',methods=['POST'])
def details():
    global name,email
    fname=request.form['fname']
    lname=request.form['lname']
    name=fname+" "+lname
    email=request.form['email']

    return render_template('app.html')



@app.route('/predict',methods=['POST'])
def predict():
    global lon,income,output
    features = [float(i) for i in request.form.values()]
    array_features = [np.array(features)]
    prediction = model.predict(array_features)
    output = prediction

    lon=request.form.get("loan")
    income=request.form.get("income")

    if output == 1:
        return render_template('yes.html',result="Yay! You are eligible to get the Loan of "+lon)
    else:
        message = 'Hello This is a Message sent from Banking Consultants. \n This Mail is sent to Mr./Ms. ' + name + ' in regards of the enquiry of loan of ' + str(
            lon) + ' \n\n\n\n Sorry You are not Eligible to get the Loan'
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("banking075@gmail.com", "Anil123.")
        server.sendmail("banking075@gmail.com", email, message)

        return render_template('no.html', result="Sorry but you can't get the Loan of "+lon)


def inte(a):
    df=pd.read_csv('static/interest.csv')
    x=df.iloc[:,0].values
    y=df.iloc[:,1].values
    mon=a
    k=0
    for i in x:
        if i==mon:
            interest=y[k]
            break
        else:
            k=k+1
    return interest



@app.route('/table',methods=['POST','GET'])
def table():
    mon=request.form['months']
    month=float(mon)

    #interest
    interest=inte(month)

    #final amount ipm=interest per month
    loan=float(lon)
    ipm=loan*interest/100
    iamt=month*ipm
    famt=iamt+loan

    #emi
    emi=famt/month

    message ='Hello This is a Message sent from Banking Consultants. \n This Mail is sent to Mr./Ms. ' +name+ ' in regards of the enquiry of loan of ' +str(lon)+ ' \n\n\n\n Hurray! You are Eligible to get the loan. \n\n\n The other details are written below \n\n\n  Loan = ' +str(lon)+ ' \n Months = ' +str(month)+ ' \n Interest Rate = '+str(interest)+' \n Final Amount to be Paid = '+str(famt)+' \n EMI = '+str(emi)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("banking075@gmail.com", "Anil123.")
    server.sendmail("banking075@gmail.com", email, message)


    return render_template('table.html',mont="The entered months are "+mon,name=name,income=income,loan=lon,interest=interest,famount=famt,emi=emi)

@app.route('/sint',methods=['POST','GET'])
def sint():
    pr=request.form['principal']
    ra=request.form['rate']
    ti=request.form['time']

    p=float(pr)
    r=float(ra)
    t=float(ti)

    tint=p*r*t/100
    tamt=tint+p

    return render_template('si res.html',tinterest=tint,tamount=tamt)

@app.route('/cint',methods=['POST','GET'])
def cint():
    pr=request.form['principal']
    ra=request.form['rate']
    ti=request.form['time']
    n=request.form['n']

    p=float(pr)
    r=float(ra)
    r=r*12/100
    t=float(ti)
    n=float(n)

    tamt=p*((1+r/n)**(t*n))
    tint=tamt-p

    return render_template('ci res.html',tinterest=tint,tamount=tamt)




if __name__ == '__main__':
    app.run(debug=True)

