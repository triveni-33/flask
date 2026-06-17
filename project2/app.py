from flask import Flask,request,redirect,url_for
app = Flask(__name__)
@app.route('/')
def home():
    return 'Triveni'

@app.route('/largest')
def largest():
    num1=int(request.args['num1'])
    num2=int(request.args['num2'])
    num3=int(request.args['num3'])
    largest=max(num1,num2,num3)
    return f'Largest:{largest}'


@app.route('/marks')
def marks():
    marks=int(request.args['marks'])
    if marks>35:
        return redirect(url_for('passed',marks=marks))
    else:
        return redirect(url_for('failed'))

@app.route('/studentpassed/<marks>')
def passed(marks):
    return f'You passed with marks {marks}'

@app.route('/studentfailed')
def failed():
    return 'You failed'
    
app.run(use_reloader=True)