from flask import Flask,render_template,url_for,redirect,request,make_response
app=Flask(__name__)
userdata={}
statements={}
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        print(request.form)
        username=request.form['username']
        useremail=request.form['useremail']
        userpassword=request.form['password']
        userpin=request.form['pinno']
        if useremail not in userdata:
            userdata[useremail]={'Username':username,'Useremail':useremail,
                             'Userpassword':userpassword,'Pinno':userpin,'Amount':0}
            return 'Registered successfully'
        else:
            return 'User already exists'
    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_useremail=request.form['useremail']
        login_password=request.form['password']
        if login_useremail in userdata:
            stored_password=userdata[login_useremail]['Userpassword']
            if stored_password==login_password:
                resp=make_response(redirect(url_for('dashboard')))
                resp.set_cookie('UserID',login_useremail)
                return resp
            else:
                return 'Invalid password'
        else:
            return 'Invalid user email'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if request.cookies.get('UserID'):
        return render_template('dashboard.html')
    else:
        return 'Please login first'

@app.route('/deposit',methods=['GET','POST'])
def deposit():
    if request.cookies.get('UserID'):
        useremail=request.cookies.get('UserID')
        if request.method=='POST':
            deposit_amount=int(request.form['amount'])
            if deposit_amount>0:
                if deposit_amount%100==0:
                    if deposit_amount <= 50000:
                        userdata[useremail]['Amount']+=deposit_amount
                        return userdata[useremail]
                    else:
                        return f'Amount should be < 50000'
                else:
                    return 'Amoount should be multiple of 100'
            else:
                return f'Amount should be greater than 0'
        return render_template('deposit.html')
    else:
        return 'Please login first to deposit'

@app.route('/withdraw',methods=['GET','POST'])
def withdraw():
    if request.cookies.get('UserID'):
        useremail=request.cookies.get('UserID')
        if request.method=='POST':
            withdraw_amount=int(request.form['amount'])
            balance_amount=userdata[useremail]['Amount']
            if withdraw_amount>0:
                if withdraw_amount%100==0:
                    if withdraw_amount <= balance_amount:
                        userdata[useremail]['Amount']-=withdraw_amount
                        return userdata[useremail]
                    else:
                        return f'No sufficent balance to withdraw'
                else:
                    return 'Amount should be multiple of 100'
            else:
                return f'Amount should be greater than 0'
        return render_template('withdraw.html')
    return f'Please login first'

@app.route('/balance')
def balance():
    if request.cookies.get('UserID'):
        useremail=request.cookies.get("UserID")
        balance_amount=userdata[useremail]['Amount']
    return render_template('balance.html',balance_amount=balance_amount)
app.run(debug=True,use_reloader=True)


