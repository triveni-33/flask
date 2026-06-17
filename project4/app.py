from flask import Flask,request,redirect,url_for,render_template,jsonify
app=Flask(__name__)  #instance means object
employeedata={} #stores emp details
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/create_employee',methods=['GET','POST'])
def create_employee():
    if request.method=='POST':
        print(request.form)
        user_name=request.form['empname']
        user_email=request.form['empmail']
        user_salary=request.form['empsalary']
        user_role=request.form['emprole']
        if user_email not in employeedata:
            employeedata[user_email]={'user_name':user_name,'user_salary':user_salary,'user_role':user_role}
            return f'employee details stored'
        else:
            return f'Employee already existed'
    return render_template('createemp.html')
@app.route('/All_empdetails',methods=['GET'])
def All_empdetails():
    return render_template('get_employees.html',employeedata=employeedata)
@app.route('/employeeupdate/<useremail>',methods=['PUT'])
def employeeupdate(useremail):
    if useremail in employeedata:
        print(request.get_json())
        updated_Empname=request.get_json()['user_name']
        updated_Empsalary=request.get_json()['user_salary']
        employeedata[useremail]['user_name']=updated_Empname
        employeedata[useremail]['user_salary']=updated_Empsalary
        return jsonify({'status':'ok'})
    else:
        return 'employee not found please check'








'''@app.route('/dummy)
def dummy():
    userdata=[(1,'vish',3000),(2,'sam',2000)]
    return render_template('dummy.html',userdata=userdata)'''
app.run(debug=True,use_reloader=True)