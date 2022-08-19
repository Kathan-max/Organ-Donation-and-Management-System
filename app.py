import errno
from sre_constants import SUCCESS
import mysql.connector
from flask import Flask, redirect, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from datetime import datetime
import yaml
app = Flask(__name__)


# db = yaml.load(open('config.yaml'))
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'Organ_Managment_Sys'
mysQl = MySQL(app)

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  password='yourpassword',
  database = 'Organ_Managment_Sys',
)

mycur = mydb.cursor(buffered=True)

@app.route('/',methods=['GET','POST'])
def index():
    if(request.method == 'POST'):
        userDetail = request.form
        name = userDetail['username']
        password = userDetail['password']
        # print("Kathan-->asda")
        cur = mysQl.connection.cursor()
        query = """SELECT * FROM login WHERE username = '%s'""" %(name)
        cur.execute(query)
        rec = cur.fetchall()
        # print("----------------")
        # print("Length: ",len(rec))
        # print("name: ",name,"--->",rec[0][0])
        # print("password: ",password,"--->",rec[0][1])
        # print("----------------")
        # print(rec)
        if(len(rec)==0):
            # print("1")
            return render_template('index.html')
        elif(password==rec[0][1]):
            # print("2")
            return home()
        else:
            # print("3")
            return render_template('index.html')
        cur.close()
    # print("4")
    return render_template('index.html')



@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('home.html')



@app.route('/Remove_<id>_data',methods=['GET','POST'])
def Remove_data(id):
    return render_template('Remove_data.html',id = id)

#    ////////////////////////////////////////    Search    ////////////////////////////////////////
# Search_User_Detail
@app.route("/search_User_details",methods=['GET','POST'])
def search_User_details():
    query = "SELECT * FROM User"
    cur = mysQl.connection.cursor()
    cur.execute(query)
    # fields = cur.column_names
    res = cur.fetchall()
    cur.close()
    return render_template('/search_and_show_list.html',res=res,fields=("User_ID", "Name", "Date_of_Birth","Medical Insurance","Medical_history","Street", "City","State"))
    
# Search_Patient_Detail
@app.route("/search_Patient_details",methods=['GET','POST'])
def search_Patient_details():
    query = "SELECT * FROM Patient"
    cur = mysQl.connection.cursor()
    cur.execute(query)
    # fields = cur.column_names
    res = cur.fetchall()
    cur.close()
    return render_template('/search_and_show_list.html',res=res,fields=("Patient_ID", "Orgen_req", "Reason of Procurement","Doctor_ID","User_ID"))


# Search_Donor_details
@app.route("/search_Donor_details",methods=['GET','POST'])
def search_Donor_details():
    query = "SELECT * FROM Donor"
    cur = mysQl.connection.cursor()
    cur.execute(query)
    # fields = cur.column_names
    res = cur.fetchall()
    cur.close()
    return render_template('/search_and_show_list.html',res=res,fields=("Donor_ID","Organ_ID" ,"Organ_donated", "Reason of Donation","Organization_ID","User_ID"))



# Search_Organ_details
@app.route("/search_Organ_details",methods=['GET','POST'])
def search_Organ_details():
    query = "SELECT * FROM Organ_available"
    cur = mysQl.connection.cursor()
    cur.execute(query)
    # fields = cur.column_names
    res = cur.fetchall()
    cur.close()
    return render_template('/search_and_show_list.html',res=res,fields=("Organ_ID", "Organ_name", "Doner_ID"))



# Search_Organization_details
@app.route("/search_Organization_details",methods=['GET','POST'])
def search_Organization_details():
    query = "SELECT * FROM Organization"
    cur = mysQl.connection.cursor()
    cur.execute(query)
    # fields = cur.column_names
    res = cur.fetchall()
    cur.close()
    return render_template('/search_and_show_list.html',res=res,fields=("Organization_ID", "Organization_name", "Location", "Government_approved"))


# Search_Organization_head_details
@app.route("/search_Organization_head_details",methods=['GET','POST'])
def search_Organization_head_details():
    query = "SELECT * FROM Organization_head"
    cur = mysQl.connection.cursor()
    cur.execute(query)
    # fields = cur.column_names
    res = cur.fetchall()
    cur.close()
    return render_template('/search_and_show_list.html',res=res,fields=("Organization_ID", "Employee_ID", "Name", "Date_of_joining","Term_Length"))



# Search_Doctor_details
@app.route("/search_Doctor_details",methods=['GET','POST'])
def search_Doctor_details():
    query = "SELECT * FROM Doctor"
    cur = mysQl.connection.cursor()
    cur.execute(query)
    # fields = cur.column_names
    res = cur.fetchall()
    cur.close()
    return render_template('/search_and_show_list.html',res=res,fields=("Doctor_ID", "Doctor_Name", "Department_Name","Organization_ID"))



# Search_Transaction_details
@app.route("/search_Transaction",methods=['GET','POST'])
def search_Transaction():
    query = "SELECT * FROM Transaction"
    cur = mysQl.connection.cursor()
    cur.execute(query)
    # fields = cur.column_names
    res = cur.fetchall()
    cur.close()
    return render_template('/search_and_show_list.html',res=res,fields=("Patient_ID","Organ_ID", "Donor_ID", "Date_of_transaction","Status"))




# Search_log
@app.route("/search_log",methods=['GET','POST'])
def search_log():
    query = "SELECT * FROM log"
    cur = mysQl.connection.cursor()
    cur.execute(query)
    # fields = cur.column_names
    res = cur.fetchall()
    cur.close()
    return render_template('/search_and_show_list.html',res=res,fields=("Querytime","Comment"))




#    ////////////////////////////////////////    Add    ////////////////////////////////////////
@app.route("/add_<id>_page",methods = ['POST','GET'])
def add_page(id):
    query = "SELECT * from " + id.capitalize()
    cur = mysQl.connection.cursor()
    cur.execute(query)
    mycur.execute(query)
    fields = mycur.column_names
    return render_template('add_page.html',success=request.args.get('success'), error=request.args.get('error'), fields = fields, id= id)

# Add user
@app.route("/add_User", methods=['POST','GET'])
def add_User():
    qry = "SELECT * from User"
    mycur.execute(qry)
    fields = mycur.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['User_ID','Medical_insurance'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)
        # val.append(temp)

    qry = "INSERT INTO User Values (%s,%s,%s,%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='User', error=error,success=success))


# Add_User_Phone_no

@app.route("/add_User_phone_no", methods=['POST','GET'])
def add_User_phone_no():
    # if not session.get('login'):
    #     return redirect( url_for('home') )
    qry = "SELECT * from User_phone_no"
    mycur.execute(qry)
    fields = mycur.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['User_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO User_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='User_phone_no', error=error,success=success))





# Add Patient

@app.route("/add_Patient", methods=['POST','GET'])
def add_Patient():
    qry = "SELECT * from Patient"
    mycur.execute(qry)
    fields = mycur.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Patient_ID','User_ID','Doctor_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Patient Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Patient', error=error,success=success))




#  Add Donor

@app.route("/add_Donor", methods=['POST','GET'])
def add_Donor():
    qry = "SELECT * from Donor"
    mycur.execute(qry)
    fields = mycur.column_names
    val = ()
    for field in fields:
        temp = request.form.get(field)
        if field not in ['Donor_ID','Organ_ID','User_ID','Organization_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)
    mycur.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Donor Values (%s,%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False

    mycur.execute("COMMIT;")

    mydb.commit()

    return redirect(url_for('add_page', id='Donor', error=error,success=success))


#  Add Doctor

@app.route("/add_Doctor", methods=['POST','GET'])
def add_Doctor():
    qry = "SELECT * from Doctor"
    mycur.execute(qry)
    fields = mycur.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Doctor_ID','Organization_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Doctor Values (%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Doctor', error=error,success=success))






# Add Doctor Phone number
@app.route("/add_Doctor_phone_no", methods=['POST','GET'])
def add_Doctor_phone_no():
    qry = "SELECT * from Doctor_phone_no"
    mycur.execute(qry)
    fields = mycur.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Doctor_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Doctor_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Doctor_phone_no', error=error,success=success))


# Add Organization
@app.route("/add_Organization", methods=['POST','GET'])
def add_Organization():
    qry = "SELECT * from Organization"
    mycur.execute(qry)
    fields = mycur.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Government_approved','Organization_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Organization Values (%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Organization', error=error,success=success))




# Add Organization phone number

@app.route("/add_Organization_phone_no", methods=['POST','GET'])
def add_Organization_phone_no():
    qry = "SELECT * from Organization_phone_no"
    mycur.execute(qry)
    fields = mycur.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Organization_ID','Phone_no'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Organization_phone_no Values (%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Organization_phone_no', error=error,success=success))



# Add Organization_Head

@app.route("/add_Organization_head", methods=['POST','GET'])
def add_Organization_head():
    qry = "SELECT * from Organization_head"
    mycur.execute(qry)
    fields = mycur.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Employee_ID','Term_length','Organization_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    qry = "INSERT INTO Organization_head Values (%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False
    mydb.commit()

    return redirect(url_for('add_page', id='Organization_head', error=error,success=success))



# Add Transaction 
@app.route("/add_Transaction", methods=['POST','GET'])
def add_Transaction_head():
    qry = "SELECT * from Transaction"
    mycur.execute(qry)
    fields = mycur.column_names

    val = ()

    for field in fields:
        temp = request.form.get(field)
        if field not in ['Patient_ID','Donor_ID','Status','Organ_ID'] and temp != '':
            temp = "\'"+temp+"\'"
        if temp == '':
            temp = 'NULL'
        val = val + (temp,)

    mycur.execute( "START TRANSACTION;" )
    qry = "INSERT INTO Transaction Values (%s,%s,%s,%s,%s,%s)"%val
    print(qry)
    success = True
    error = False
    try:
        mycur.execute(qry)
    except:
        print("Error : User not Inserted")
        error = True
        success = False

    mydb.commit()

    return redirect(url_for('add_page', id='Transaction', error=error,success=success))




#    ////////////////////////////////////////    Update    ////////////////////////////////////////



@app.route("/update_user_page",methods = ['POST','GET'])
def update_user_page():
    qry_upd = "Select * from User"
    mycur.execute(qry_upd)
    fields_upd = mycur.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_user_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_user_details",methods = ['GET','POST'])
def update_details():
    mycur.execute("SELECT * from User")
    fields = mycur.column_names
    qry = "UPDATE User SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['User_ID','Medical_insurance']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE User_ID = %s;" %(request.form['User_ID'])
    print(qry)
    try:
        mycur.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from User where User_ID = %s" %(request.form['User_ID'])
    mycur.execute(qry2)
    res = mycur.fetchone()
    qry = "Select * from User where User.User_ID = %s" %(request.form['User_ID'])
    qry1 = "Select * from User_phone_no where User_ID = %s" %(request.form['User_ID'])
    mycur.execute(qry)
    not_found=False
    res=()
    if(mycur.rowcount > 0):
        res = mycur.fetchone()
    else:
        not_found=True
    fields = mycur.column_names
    qry_upd = "Select * from User where User_ID = %s" %(request.form['User_ID'])
    mycur.execute(qry_upd)
    upd_res = ()
    if(mycur.rowcount > 0):
        upd_res = mycur.fetchone()
    fields_upd = mycur.column_names
    mycur.execute(qry1)
    phone_no = mycur.fetchall()
    qry_pat = "select Patient_ID, organ_req, reason_of_procurement, Doctor_name from Patient inner join Doctor on Doctor.Doctor_ID = Patient.Doctor_ID and User_ID = %s" %(request.form['User_ID'])
    qry_don = "select Donor_ID, organ_donated,organ_ID, reason_of_donation, Organization_name from Donor inner join Organization on Organization.Organization_ID = Donor.Organization_ID and User_ID = %s" %(request.form['User_ID'])
    # qry_trans = "select distinct Transaction.Patient_ID, Transaction.Donor_ID, Organ_ID, Date_of_transaction, Status from Transaction, Patient, Donor where (Patient.User_ID = %s and Patient.Patient_ID = Transaction.Patient_ID) or (Donor.User_Id= %s and Donor.Donor_ID = Transaction.Donor_ID)" %((request.form['User_ID']),(request.form['User_ID']))
    #
    res_pat = ()
    res_dnr = ()
    # res_trans = ()
    mycur.execute(qry_pat)
    if(mycur.rowcount > 0):
        res_pat = mycur.fetchall()
    fields_pat = mycur.column_names
    #
    mycur.execute(qry_don)
    if(mycur.rowcount > 0):
        res_dnr = mycur.fetchall()
    fields_dnr = mycur.column_names
    # mycur.execute(qry_trans)
    # if(mycur.rowcount > 0):
        # res_trans = mycur.fetchall()
    # fields_trans = mycur.column_names
    # if("show" in request.form):
    # res_trans = res_trans,fields_trans = fields_trans,
    return render_template('show_detail_2.html',res = res,fields = fields, not_found=not_found, phone_no = phone_no, res_dnr = res_dnr, res_pat = res_pat, fields_dnr = fields_dnr, fields_pat = fields_pat)
    # return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_patient_page",methods = ['POST','GET'])
def update_patient_page():
    qry_upd = "Select * from Patient"
    mycur.execute(qry_upd)
    fields_upd = mycur.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_patient_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_patient_details",methods = ['GET','POST'])
def update_patient_details():
    mycur.execute("SELECT * from Patient")
    fields = mycur.column_names
    qry = "UPDATE Patient SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['User_ID','Doctor_ID','Patient_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Patient_ID = %s and organ_req = \'%s\';" %(request.form['Patient_ID'],request.form['organ_req'])
    print(qry)
    try:
        mycur.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from Patient WHERE Patient_ID = %s and organ_req = \'%s\';" %(request.form['Patient_ID'],request.form['organ_req'])
    mycur.execute(qry2)
    res = mycur.fetchone()
    print(res)
    print(qry2)
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_donor_page",methods = ['POST','GET'])
def update_donor_page():
    qry_upd = "Select * from Donor"
    mycur.execute(qry_upd)
    fields_upd = mycur.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_donor_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_donor_details",methods = ['GET','POST'])
def update_donor_details():
    mycur.execute("SELECT * from Donor")
    fields = mycur.column_names
    qry = "UPDATE Donor SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['User_ID','Organization_ID','Donor_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Donor_ID = %s and organ_donated = \"%s\";" %(request.form['Donor_ID'],request.form['organ_donated'])
    print(qry)
    try:
        mycur.execute(qry)
    except:
        print("update error")
    mydb.commit()
    qry2 = "select * from Patient WHERE Donor_ID = %s and organ_donated = \"%s\";" %(request.form['Donor_ID'],request.form['organ_donated'])
    mycur.execute(qry2)
    res = mycur.fetchone()
    print(res)
    print(qry2)
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_doctor_page",methods = ['POST','GET'])
def update_doctor_page():
    qry_upd = "Select * from Doctor"
    mycur.execute(qry_upd)
    fields_upd = mycur.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_doctor_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_doctor_details",methods = ['GET','POST'])
def update_doctor_details():
    mycur.execute("SELECT * from Doctor")
    fields = mycur.column_names
    qry = "UPDATE Doctor SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['Doctor_ID','Organization_ID']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Doctor_ID = %s;" %(request.form['Doctor_ID'])
    print(qry)
    try:
        mycur.execute(qry)
    except:
        print("update error")
        return render_template('error_page.html')
    mydb.commit()
    qry2 = "select * from Doctor WHERE Doctor_ID = %s;" %(request.form['Doctor_ID'])
    mycur.execute(qry2)
    res = mycur.fetchone()
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)

@app.route("/update_organization_page",methods = ['POST','GET'])
def update_organization_page():
    qry_upd = "Select * from Organization"
    mycur.execute(qry_upd)
    fields_upd = mycur.column_names
    upd_res=[None]*len(fields_upd)
    return render_template('update_organization_page.html',fields = fields_upd,res = upd_res)

@app.route("/update_organization_details",methods = ['GET','POST'])
def update_organization_details():
    mycur.execute("SELECT * from Organization")
    fields = mycur.column_names
    qry = "UPDATE Organization SET "
    for field in fields:
        if request.form[field] not in ['None','']:
            if field in ['Organization_ID','Government_approved']:
                qry = qry + "%s = %s , " %(field,request.form[field])
            else:
                qry = qry + " %s = \'%s\' , " %(field,request.form[field])
        else:
            qry = qry + "%s = NULL , " %(field)
    qry = qry[:-2]
    qry = qry + "WHERE Organization_ID = %s;" %(request.form['Organization_ID'])
    print(qry)
    try:
        mycur.execute(qry)
    except:
        print("update error")
        return render_template('error_page.html')
    mydb.commit()
    qry2 = "select * from Organization WHERE Organization_ID = %s;" %(request.form['Organization_ID'])
    mycur.execute(qry2)
    res = mycur.fetchone()
    return render_template("show_detail.html",res = res,fields=fields,not_found = False)


#  Remove Page

@app.route('/remove_user',methods=['GET','POST'])
def remove_user():
    return render_template('/remove_user.html')

@app.route('/remove_patient',methods=['GET','POST'])
def remove_hostel():
    return render_template('/remove_patient.html')

@app.route('/remove_donor',methods=['GET','POST'])
def remove_room():
    return render_template('/remove_donor.html')

@app.route('/remove_doctor',methods=['GET','POST'])
def remove_doctor():
    return render_template('/remove_doctor.html')

@app.route('/remove_organization',methods=['GET','POST'])
def remove_organization():
    return render_template('/remove_organization.html')

@app.route('/remove_organization_head',methods=['GET','POST'])
def remove_organization_head():
    return render_template('/remove_organization_head.html')


#----------------Actual Deletion from database------------------------

@app.route('/del_user',methods=['GET','POST'])
def del_hostel():
    qry = "call remove_User("+str(request.form['User_ID'])+ ");"
    print(qry)
    try:
        mycur.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    # redirect(url_for('add_page', id='User', error=error,success=success))
    return redirect( url_for('Remove_data',id='User'))


@app.route('/del_patient',methods=['GET','POST'])
def del_patient():
    qry = "call remove_Patient("+str(request.form['Patient_ID'])+", "+ "\'" +str(request.form['organ_req']) + "\'" + ");"
    print(qry)
    try:
        mycur.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('Remove_data',id='Patient'))

@app.route('/del_donor',methods=['GET','POST'])
def del_donor():
    # qry = "delete from Donor where Donor_ID="+str(request.form['Donor_ID'])+" and organ_donated=\'%s\'" %request.form['organ_donated']
    # call remove_Donor(5,'Kidney');
    qry = "call remove_donor("+str(request.form['Donor_ID'])+", "+ "\'" +str(request.form['organ_donated']) + "\'" + ");"
    try:
        mycur.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('Remove_data',id='Donor'))


@app.route('/del_doctor',methods=['GET','POST'])
def del_doctor():
    qry = "call remove_Doctor(" + str(request.form['Doctor_ID'])+");"
    try:
        mycur.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('Remove_data',id='Doctor'))




@app.route('/del_organization',methods=['GET','POST'])
def del_organization():
    qry = "call remove_Organization("+str(request.form['Organization_ID']) + ");"
    try:
        mycur.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('Remove_data',id='Organization'))


@app.route('/del_organization_head',methods=['GET','POST'])
def del_organization_head():
    # qry = "delete from Organization_head where Organization_ID="+str(request.form['Organization_ID'])+" and Employee_ID="+str(request.form['Employee_ID'])
    qry = "call remove_Organization_Head(" + str(request.form['Organization_ID']) + "," + str(request.form['Employee_ID']) + ");"
    try:
        mycur.execute(qry)
    except:
        print("Error in deletion")
    mydb.commit()
    return redirect( url_for('Remove_data',id='Organization Head'))




# -------------------------------------------------
# Search Detail
@app.route("/search_detail",methods = ['POST','GET'])
def search_detail():
    return render_template('search_detail.html')


# Logout Process
@app.route("/logout", methods = ['GET','POST'])
def logout():
    return render_template('index.html');

if(__name__ =='__main__'):
    app.run(debug=True)
