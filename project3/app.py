from flask import Flask,request,redirect,url_for
app=Flask(__name__)
@app.route('/')
def home():
    return '''<center> <h1>Hello user</h1><br>
              <h1>use the given url for URL convertion </h1><br>
              <ul><li>/userage/&ltintvalue&gt</li><br>
              <li>/userheight/&ltfloatvalue&gt</li><br>
              <li>username/&ltname&gt<li><br>
              <li>username/&ltimepath&gt</li><br>
              <li>/unique/&ltuuidvalue&gt</li></ul><br> 
              </center>'''
@app.route('/userage/<int:var>')
def userage(var):
    print(type(var))
    return f'User age is {var}'
app.run(use_reloader=True)

@app.route('/userheight/<float:var>')
def userheight(var):
    print(type(var))
    return f'User height is {var}'
app.run(use_reloader=True)

@app.route('/username/<var>')
def username(var):
    print(type(var))
    return f'User height is {var}'
app.run(use_reloader=True)

@app.route('/userimg/<path :filepath>')
def userimg(filepath):
    #print(type(var))
    return f'The given filepath is {filepath}'
app.run(use_reloader=True)

