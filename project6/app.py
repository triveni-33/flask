from flask import Flask,request,redirect,url_for,render_template,flash,session
import flask_excel as excel
from flask_session import Session
from otp import genotp
from cmail import send_mail
from stoken import endata,dndata
from mysql.connector import (connection)
mydb=connection.MySQLConnection(user='root',host='localhost',password='Triveni@2005',database='mynotes')
app=Flask(__name__)
excel.init_excel(app)
app.secret_key='triveni123'
app.config['SESSION_TYPE']='filesystem'
Session(app)
@app.route('/',methods=['GET'])
def home():
    return render_template('Welcome.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        useremail=request.form['useremail']
        userpassword=request.form['password']
        gotp=genotp() #calling the function
        userdetails={'username':username,'useremail':useremail,'userpassword':userpassword,'userotp':gotp}
        subject='User validation OTP for SNM'
        body=f'Use the give otp {gotp}'
        send_mail(to=useremail,subject=subject,body=body)
        flash('OTP has been sent given mail')
        return redirect(url_for('otpverify',serverdata=endata(data=userdetails)))
    return render_template('registerform.html')
@app.route('/otpverify/<serverdata>',methods=['GET','POST'])
def otpverify(serverdata):
    if request.method=='POST':
        try:
            user_details=dndata(data=serverdata) #{'username':username,'useremail':useremail,'userpassword':userpassword,'userotp':gotp}
        except Exception as e:
            print('Error in deserializing data',str(e))
            return redirect(url_for('register'))
        userotp=request.form['otp']
        if user_details['userotp']==userotp:
            try:
                #DB connection
                cursor=mydb.cursor(buffered=True) #which used to interact with mysql server
                cursor.execute('insert into userdata(username,useremail,userpassword) values(%s,%s,%s)',[user_details['username'],user_details['useremail'],user_details['userpassword']])
                mydb.commit() #to save the insert command permanently
                cursor.close()
            except Exception as e:
                print('MYSQL ERROR ',str(e))
                flash('Cannot store the details')
                return redirect(url_for('otpverify',serverdata=serverdata))
            else:
                flash('user Register Successfully')
                return redirect(url_for('login'))
        else:
            flash('OTP was Wrong')
            return redirect(url_for('otpverify',serverdata=serverdata))
    return render_template('otp.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        login_useremail=request.form['useremail']
        login_userpassword=request.form['password']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from userdata where useremail=%s',[login_useremail])
            email_count=cursor.fetchone() #(1,) or (0,)
        except Exception as e:
            print('Mysql ERROR :',str(e))
            flash('Could not verify email')
            return redirect(url_for('login'))
        else:
            if email_count[0] > 0:
                cursor.execute('select userpassword from userdata where useremail=%s',[login_useremail])
                stored_password=cursor.fetchone() #(123,)
                cursor.close()
                if stored_password[0]==login_userpassword:
                    print(session,'before session')
                    session['user']=login_useremail
                    print(session,'after session')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Password was wrong')
                    return redirect(url_for('login'))
            elif email_count[0] <= 0:
                flash('No Email found pls check')
                return redirect(url_for('login'))
    return render_template('login.html')
@app.route('/dashboard',methods=['GET'])
def dashboard():
    return render_template('dashboard.html')
@app.route('/addnotes',methods=['GET','POST'])
def addnotes():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    if request.method=='POST':
        notes_title=request.form['title']
        notes_desc=request.form['description']
        try:
            useremail=session.get('user')
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[useremail])
            user_id=cursor.fetchone()[0] #(1,) #none[0]
            cursor.execute('insert into notesdata(title,description,userid) values(%s,%s,%s)',[notes_title,notes_desc,user_id])
            mydb.commit()
            cursor.close()
        except Exception as e:
            print('MYSQL Error:',str(e))
            flash('Could save notes')
            return redirect(url_for('addnotes'))
        else:
            flash('Notes details successfully stored')
            return redirect(url_for('addnotes'))
    return render_template('addnotes.html')
@app.route('/viewallnotes',methods=['GET'])
def viewallnotes():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        useremail=session.get('user')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[useremail])
        user_id=cursor.fetchone()[0] #(1,) #none[0]
        cursor.execute('select notesid,title,created_at from notesdata where userid=%s',[user_id])
        allnotesdata=cursor.fetchall() #[(1,'Mysql','2026-06-12'),(2,'Python','2026-06-12'),]
        print(allnotesdata)
        cursor.close()
    except Exception as e:
        print('MYsql Error:',str(e))
        flash('Could not fetch the notes details')
        return redirect(url_for('dashboard'))
    else:
        return render_template('viewallnotes.html',allnotesdata=allnotesdata)
@app.route('/viewnotes/<nid>',methods=['GET'])
def viewnotes(nid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        useremail=session.get('user')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[useremail])
        user_id=cursor.fetchone()[0] #(1,) #none[0]
        cursor.execute('select notesid,title,description,created_at from notesdata where userid=%s and notesid=%s',[user_id,nid])
        notesdata=cursor.fetchone() #(1,'Mysql','2026-06-12'),
        print(notesdata)
        cursor.close()
    except Exception as e:
        print('MYsql Error:',str(e))
        flash('Could not fetch the notes details')
        return redirect(url_for('dashboard'))
    else:
        return render_template('viewnotes.html',notesdata=notesdata)
    
@app.route('/deletenotes/<nid>',methods=['GET'])
def deletenotes(nid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
            useremail = session.get('user')
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s', [useremail])
            user_id = cursor.fetchone()[0]
            cursor.execute('delete from notesdata where notesid=%s and userid=%s', [nid, user_id])
            mydb.commit()
            cursor.close()
    except Exception as e:
            print('Mysql Error:', str(e))
            flash('Could not delete the note')
            return redirect(url_for('viewallnotes'))
    else:
            flash('Note deleted successfully')
            return redirect(url_for('viewallnotes'))
    
@app.route('/updatenotes/<nid>',methods=['GET','POST'])
def updatenotes(nid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        useremail=session.get('user')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[useremail])
        user_id=cursor.fetchone()[0]
        cursor.execute('select notesid,title,description,created_at from notesdata where userid=%s and notesid=%s',[user_id,nid])
        stored_notesdata=cursor.fetchone()
        cursor.close()
    except Exception as e:
        print('Mysql Error:',str(e))
        flash('Could not fetch the notes details')
        return redirect(url_for('dashboard'))
    else:
        if request.method=='POST':
            updated_title=request.form['title']
            updates_description=request.form['description']
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update notesdata set title=%s,description=%s where notesid=%s and userid=%s',[updated_title,updates_description,nid,user_id])
                mydb.commit()
                cursor.close()
            except Exception as e:
                print(e)
                flash('could not update notes details')
                return redirect(url_for('updatenotes',nid=nid))
            else:
                flash('Notes updated successfully')
                return redirect(url_for('updatenotes',nid=nid))
        return render_template('updatenotes.html',stored_notesdata=stored_notesdata)

@app.route('/Getexceldata',methods=['GET'])    
def Getexceldata():
    if not session.get('user'):
        flash('please login first') 
        return redirect(url_for('login'))
    try:
        useremail=session.get('user')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[useremail])
        user_id=cursor.fetchone()[0] #(1,) #none[0]
        #cursor.execute('select notesid,title,created_at from notesdata where userid=%s',[user_id])
        cursor.execute('select notesid,title,description,created_at from notesdata where userid=%s',[user_id])
        stored_allnotesdata=cursor.fetchall() #[(1,'Mysql','2026-06-12'),(2,'Python','2026-06-12'),]
        print(stored_allnotesdata)
        cursor.close()
    except Exception as e:
        print('MYsql Error:',str(e))
        flash('Could not fetch the notes details')
        return redirect(url_for('dashboard'))
    else:
        notesdata=[list(i) for i in stored_allnotesdata]
        columns=['Notesid','Title','description','created_at']
        notesdata.insert(0,columns)
        return excel.make_response_from_array(notesdata,'xlsx',file_name='Notesdata')

@app.route('/fileupload', methods=['GET', 'POST'])
def fileupload():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))   
    if request.method=='POST':
        filedata = request.files['file']
        fdata = filedata.read()
        fname = filedata.filename
        try:
            useremail = session.get('user')
            cursor = mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s', [useremail])
            user_id = cursor.fetchone()[0]  # #(1,) #none[0]
            cursor.execute('insert into filesdata(filename,filedata,userid) values(%s,%s,%s)', [fname, fdata, user_id])
            mydb.commit()
            cursor.close() 
        except Exception as e:
            print('Mysql Error', str(e))
            flash('Could not save file data')
            return redirect(url_for('fileupload'))   
        else:
            flash('File uploaded successfully')
            return redirect(url_for('fileupload')) 
    return render_template('uploadfile.html')

@app.route('/viewallfiles',methods=['GET'])
def viewallfiles():
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        useremail=session.get('user')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s',[useremail])
        user_id=cursor.fetchone()[0] #(1,) #none[0]
        cursor.execute('select fileid,filename,created_at from filesdata where userid=%s',[user_id])
        allfilesdata=cursor.fetchall() #[(1,'Mysql','2026-06-12'),(2,'Python','2026-06-12'),]
        print(allfilesdata)
        cursor.close()
    except Exception as e:
        print('MYsql Error:',str(e))
        flash('Could not fetch the notes details')
        return redirect(url_for('dashboard'))
    else:
        return render_template('viewallfiles.html',allfilesdata=allfilesdata)
    
@app.route('/deletefile/<fid>',methods=['GET'])
def deletefile(fid):
    if not session.get('user'):
        flash('pls login first')
        return redirect(url_for('login'))
    try:
        useremail = session.get('user')
        cursor = mydb.cursor(buffered=True)
        cursor.execute('select userid from userdata where useremail=%s', [useremail])
        user_id = cursor.fetchone()[0]
        cursor.execute('delete from filesdata where fileid=%s and userid=%s', [fid, user_id])
        mydb.commit()
        cursor.close()
    except Exception as e:
        print('Mysql Error:', str(e))
        flash('Could not delete the file')
        return redirect(url_for('viewallfiles'))
    else:
        flash('File deleted successfully')
        return redirect(url_for('viewallfiles'))


if __name__=='__main__':
    app.run(debug=True,use_reloader=True)