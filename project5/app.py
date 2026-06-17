from flask import Flask, render_template, request, redirect, url_for,render_template
from cmail import send_mail
from otp import generate_otp
import otp
app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('Welcome.html')
@app.route('/otp',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        useremail=request.form['useremail']
        userpassword=request.form['userpassword']
        otp()=generate_otp()
        subject='User validation OTP for SNM'
    
        
        return 'OTP SENT'
    return render_template('registerform.html')
if __name__=='__main__':
    app.run(debug=True,use_reloader=True)