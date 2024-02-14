from flask import render_template, request, redirect
from flask import current_app as app
from application.model import *
from application.functions import *




# Log in page
@app.route("/",methods=["GET", "POST"])
def home():
    AE = UE = "Enter Email or Username"
    AP = UP = "Enter Password"

    if request.method == "GET":  
        return render_template("index.html",AE=AE,UE=UE,AP=AP,UP=UP)
    
    elif request.method == "POST":
        if request.form['type'] == "Manager":
            present = Manager.query.filter_by(email = request.form["femail"]).first()

            if not present:
                present = Manager.query.filter_by(username = request.form["femail"]).first()
            
            if present:
                if present.password != request.form["fpass"]:
                    return render_template("index.html",AE=request.form["femail"],AP=request.form["fpass"],UE=UE,UP=UP,data=1)
                else:
                    return redirect("/Manager/"+present.m_id+encode(present.password)+"/Dashboard")
            
            else:
                return render_template("index.html",AE=request.form["femail"],AP=request.form["fpass"],UE=UE,UP=UP,data=0)
        

        elif request.form['type'] == "Customer":
            present = Customer.query.filter_by(email = request.form["femail"]).first()

            if not present:
                present = Customer.query.filter_by(username = request.form["femail"]).first()
            
            if present:
                if present.password != request.form["fpass"]:
                    return render_template("index.html",UE=request.form["femail"],UP=request.form["fpass"],AE=AE,AP=AP,data2=1)
                else:
                    return redirect("/Member/"+present.c_id+encode(present.password)+"/Store")
            
            else:
                return render_template("index.html",UE=request.form["femail"],UP=request.form["fpass"],AE=AE,AP=AP,data2=0)
        



