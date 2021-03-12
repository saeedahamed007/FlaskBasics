from flask import *  
import sqlite3  
  
app = Flask(__name__)  
 

''' To build a CRUD application in the flask, 
we must focus on the view functions (to take the input) and the controllers (to save that data into the database).
Let us look at the view function: index() which is associated with the URL (/).
 It renders a template index.html. '''



@app.route("/")  
def index():  
    return render_template("index.html");  
 

''' The view function add() which is associated with the URL (/add) renders the template add.html given below. 
    It provides the form to enter the employee information. '''

@app.route("/add")  
def add():  
    return render_template("add.html")  


'''  All the details entered by the Admin is posted to the URL /savedetails which is associated with the
function saveDetails(). 
The function saveDetails() is given below which contains the code for extracting 
the data entered by the admin and save that data into the table Employees.
It also generates the message depending upon the cases in which the data is successfully inserted,
or some error occurred  '''



@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"  
    if request.method == "POST":  
        try:  
            name = request.form["name"]  
            email = request.form["email"]  
            address = request.form["address"]  
            with sqlite3.connect("employee.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into Employees (name, email, address) values (?,?,?)",(name,email,address))  
                con.commit()  
                msg = "Employee successfully Added"  
        except:  
            con.rollback()  
            msg = "We can not add the employee to the list"  
        finally:  
            return render_template("success.html",msg = msg)  
            con.close()  



'''  The template delete_record.html contains a link to the URL /view which shows the Employee records to the admin.
It is associated with the function view() which establishes the connection to the database, 
fetch all the information and pass that information to the HTML template view.html to display on the client side browser. '''



@app.route("/view")  
def view():  
    con = sqlite3.connect("employee.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees")  
    rows = cur.fetchall()  
    return render_template("view.html",rows = rows)  



'''  The Employee_Id entered by the admin is posted to the URL /deleterecord which contains the python 
code to establish the connection to the database and then delete all the records for the specified Employee ID. 
The URL /deleterecord is associated with the function deleterecord() which is given below.  '''


@app.route("/delete")  
def delete():  
    return render_template("delete.html")  
 
@app.route("/deleterecord",methods = ["POST"])  
def deleterecord():  
    id = request.form["id"]  
    with sqlite3.connect("employee.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Employees where id = ?",id)  
            msg = "record successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return render_template("delete_record.html",msg = msg)  
  
if __name__ == "__main__":  
    app.run(debug = True)