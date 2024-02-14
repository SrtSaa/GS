from flask import render_template, request, redirect
from flask import current_app as app
from application.model import *
from application.functions import *
import datetime as d





# Memeber dashboard
@app.route("/Member/<string:code>/Store",methods=["GET", "POST"])
def customer_home(code):
    if not match(code,5):
        return redirect("/unknown")

    dictn = find_items2()

    if request.method == "GET":  
        return render_template("store.html",code=code,d=dictn,id=0)
    
    if request.method == "POST":  
        id = int(request.form['id'])
        if id==1:
            return render_template("store.html",code=code,d=dictn,id=1)
        if id==2:
            search = request.form['q']
            dictn = find_items3(search)
            if len(dictn) != 0:
                return render_template("store.html",code=code,d=dictn,id=2,q=search)
            dictn = find_items2(search)
            return render_template("store.html",code=code,d=dictn,id=2,q=search)



# Category wise items
@app.route("/Member/<string:code>/Store/<string:category>",methods=["GET", "POST"])
def view_category(code,category):
    if not match(code,5):
        return redirect("/unknown")
    items = Item.query.all()
    dictn = {}
    dictn[category] = []
    for i in items:
        if category == i.cat_name:
            dictn[category].append(i)
    if request.method == "GET":  
        return render_template("store.html",code=code,d=dictn,id=3)



# Memeber Cart
@app.route("/Member/<string:code>/Cart",methods=["GET", "POST"])
def view_cart(code):
    if not match(code,5):
        return redirect("/unknown")


    if request.method == "GET":  
        return render_template("cart.html",code=code)
    
    if request.method == "POST":
        ids = request.form['ids']
        if len(ids)>0:
            ids = ids.split(',')

        l = []
        for i in ids:
            items = Item.query.filter_by(i_id=i).first()
            l.append(items)

        return render_template("cart.html",code=code,items=l)



# calculate the sell
@app.route("/Member/<string:code>/Sell",methods=["GET", "POST"])
def cal_sell(code):
    if not match(code,5):
        return redirect("/unknown")

    if request.method == "POST":
        ids = request.form['ids']
        qty = request.form['qty']
        ids = ids.split(',')
        qty = qty.split(',')
        

        sell = Sell.query.all()
        if len(sell)!=0:
            sid = sell[-1].s_id
        else:
            sid = 'S000000'

        for i in range(len(ids)):
            sid = str(int(sid[1:])+1)
            sid = 'S'+'0'*(6-len(sid))+sid
            item = Item.query.filter_by(i_id=ids[i]).first()

            sitem = Sell()
            sitem.s_id = sid
            sitem.c_id = code[:5]
            sitem.cat_id = item.cat_id
            sitem.cat_name = item.cat_name
            sitem.i_id = item.i_id
            sitem.i_name = item.i_name
            sitem.date = str(d.date.today())
            sitem.quantity = item.quantity
            sitem.unit = item.unit  
            if item.stock < 15:
                sitem.price = item.price + 10
            else:
                sitem.price = item.price
            sitem.selling_quantity = int(qty[i])
            if item.stock < 15:
                sitem.profit = (item.price + 10) * int(qty[i])
            else:   
                sitem.profit = item.price * int(qty[i])
            db.session.add(sitem)
            item.stock = item.stock - int(qty[i])
            db.session.add(item)
        
        cus = Customer.query.filter_by(c_id=code[:5]).first()
        cus.no_purchase = cus.no_purchase + 1
        db.session.add(cus)

        db.session.commit()

        return redirect("/Member/"+code+"/Store")



# Profile
@app.route("/Member/<string:code>/Profile",methods=["GET", "POST"])
def view_profile(code):
    if not match(code,5):
        return redirect("/unknown")
    
    cus = Customer.query.filter_by(c_id=code[:5]).first()
    if request.method == "GET":  
        return render_template("details.html",code=code,person=cus,u=2,e=0)
    


# Update profile
@app.route("/Member/<string:code>/Profile/update",methods=["GET", "POST"])
def update_profile(code):
    if not match(code,5):
        return redirect("/unknown")
    
    person = Customer.query.filter_by(c_id=code[:5]).first ()
    if request.method == "GET":  
        return render_template("details.html",code=code,person=person,u=2,e=1)
    
    if request.method == "POST":  
        person.password = request.form['fpass']
        db.session.add(person)
        db.session.commit()
        code = person.c_id+encode(request.form['fpass'])
        return redirect("/Member/"+code+"/Profile")



# Register new member
@app.route("/Register",methods=["GET", "POST"])
def register():
    if request.method == "GET":  
        return render_template("add_customer.html",f=0)

    elif request.method == "POST":  
        uname = request.form["uname"]        
        fname = request.form["fname"]
        lname = request.form["lname"]
        gen = request.form["gen"]
        dob = request.form["dob"]
        mobile = request.form["mobile"]
        email = request.form["femail"]        
        pw = request.form["fpass"]

        cus = Customer.query.filter_by(username=uname).first()
        if cus:
            return render_template("add_customer.html",f=1,fname=fname,lname=lname,dob=dob,mobile=mobile,email=email)
        cus = Customer.query.filter_by(mobile=mobile).first()
        if cus:
            return render_template("add_customer.html",f=2,fname=fname,lname=lname,dob=dob,mobile=mobile,email=email)
        cus = Customer.query.filter_by(email=email).first()
        if cus:
            return render_template("add_customer.html",f=3,uname=uname,fname=fname,lname=lname,dob=dob,mobile=mobile,email=email)

        cuss = Customer.query.all()
        if len(cuss)!=0:
            cid = cuss[-1].c_id
        else:
            cid = 'C0000'
        cid = str(int(cid[1:])+1)
        cid = 'C'+'0'*(4-len(cid))+cid


        cus = Customer()
        cus.c_id = cid
        cus.f_name = fname
        cus.l_name = lname
        cus.gender = gen
        cus.dob = dob
        cus.mobile = mobile
        cus.email = email
        cus.username = uname
        cus.password = pw
        cus.no_purchase = 0

        db.session.add(cus)
        db.session.commit()
        return redirect("/")



# Register new member
@app.route("/Member/<string:code>/History",methods=["GET", "POST"])
def history(code):
    sell = Sell.query.filter_by(c_id = code[:5]).all()
    s, d = set(), {}
    for item in sell:
        if item.date not in s:
            s.add(item.date)
    l = list(s)
    print(l)
    l.sort(reverse=True)
    print(l)
    for i in l:
        d[i] = []
    for item in sell:
        d[item.date].append(item)
    print(d)
    if request.method == "GET":  
        return render_template("history.html",code=code,d=d)


