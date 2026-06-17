from flask import Flask,request #defining Flask class from flask library
app=Flask(__name__) #creating api instance using Flask class

@app.route('/') #defining URL using decorator
def home(): #associating a function for Url
    return 'WELCOME TO FLASK' #logic

@app.route('/second')
def second():
    return 'We are in second page'

@app.route('/username')
def username():
    print(request.args)
    name=request.args['name']
    return f'Hello {name}'

@app.route('/agevalidator')
def agevalidator():
    print(request.args)
    userage=request.args.get('age')
    if userage:
        if int(userage)>18:
            return 'Eligible'
        else:
            return 'not eligible'
    else:
        return 'invalid input'
    #return f'your age : {age}'

app.run() #running application