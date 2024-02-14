from flask import render_template, request, redirect
from flask import current_app as app
from application.model import *
from application.functions import *
import matplotlib.pyplot as plt




# Manager dashboard
@app.route("/Manager/<string:code>/Dashboard",methods=["GET", "POST"])
def manager_home(code):
    if not match(code,4):
        return redirect("/unknown")

    if request.method == "GET":  
        manager = Manager.query.filter_by(m_id=code[:4]).first()
        return render_template("manager_home.html",code=code,name=manager.f_name+" "+manager.l_name)



# Inventory
@app.route("/Manager/<string:code>/Inventory",methods=["GET", "POST"])
def inventory(code):
    if not match(code,4):
        return redirect("/unknown")

    dictn = find_items()
    if request.method == "GET":  
        return render_template("inventory.html",code=code,d=dictn,id=0)
    
    if request.method == "POST":  
        id = int(request.form['id'])
        if id==1:
            return render_template("inventory.html",code=code,d=dictn,id=1)
        if id==2:
            search = request.form['q']
            dictn = find_items3(search)
            if len(dictn) != 0:
                return render_template("inventory.html",code=code,d=dictn,id=2,q=search)
            dictn = find_items(search)
            return render_template("inventory.html",code=code,d=dictn,id=2,q=search)



# Category wise items
@app.route("/Manager/<string:code>/Inventory/<string:category>",methods=["GET", "POST"])
def viewCategory(code,category):
    if not match(code,4):
        return redirect("/unknown")
    items = Item.query.all()
    dictn = {}
    dictn[category] = []
    for i in items:
        if category == i.cat_name:
            dictn[category].append(i)

    if request.method == "GET":  
        return render_template("inventory.html",code=code,d=dictn,id=3)



# Item Details
@app.route("/Manager/<string:code>/Inventory/<string:id>/Details",methods=["GET", "POST"])
def view_Item(code,id):
    if not match(code,4):
        return redirect("/unknown")
    
    item = Item.query.filter_by(i_id=id).first()

    if request.method == "GET":  
        return render_template("item_details.html",code=code,item=item,e=0)



# Update Item Details
@app.route("/Manager/<string:code>/Inventory/<string:id>/Update",methods=["GET", "POST"])
def update_Item(code,id):
    if not match(code,4):
        return redirect("/unknown")
    
    item = Item.query.filter_by(i_id=id).first()

    if request.method == "GET":  
        return render_template("item_details.html",code=code,item=item,e=1)

    if request.method =="POST":
        item.stock = request.form['stock']
        item.price = request.form['price']
        db.session.add(item)
        db.session.commit()
        return redirect("/Manager/"+code+"/Inventory/"+id+"/Details")



# Add Item Details
@app.route("/Manager/<string:code>/Inventory/Item/Add",methods=["GET", "POST"])
def add_Item(code):
    if not match(code,4):
        return redirect("/unknown")
    
    if request.method == "GET":
        catgs = Category.query.all()
        return render_template("add_item.html",code=code,catgs=catgs)
    
    if request.method == "POST":
        its = Item.query.all()
        if len(its)!=0:
            iid = its[-1].i_id
        else:
            iid = 'C0000'
        iid = str(int(iid[1:])+1)
        iid = 'I'+'0'*(5-len(iid))+iid

        item = Item()
        item.i_id = iid
        item.i_name = request.form["iname"]  
        item.cat_id = request.form["cname"][:7]  
        item.cat_name = request.form["cname"][8:] 
        item.quantity = request.form["qty"]  
        item.unit = request.form["unit"]  
        item.price = request.form["price"]  
        item.stock = request.form["stock"]  
        item.mfg_date = request.form["mfg"]  
        item.exp_date = request.form["exp"]  

        db.session.add(item)
        db.session.commit()

        return redirect("/Manager/"+code+"/Dashboard")



# Delete Item
@app.route("/Manager/<string:code>/Inventory/<string:id>/Delete",methods=["GET", "POST"])
def delete_Item(code,id):
    if not match(code,4):
        return redirect("/unknown")
    
    if request.method == "GET":  
        item = Item.query.filter_by(i_id=id).first()
        db.session.delete(item)
        db.session.commit()
        return redirect("/Manager/"+code+"/Inventory")
    


# Add Category
@app.route("/Manager/<string:code>/Category/Add",methods=["GET", "POST"])
def add_category(code):
    if not match(code,4):
        return redirect("/unknown")

    if request.method == "GET":
        return render_template("category.html",code=code,c=1)

    if request.method == "POST":
        s = request.form["cname"]
        s = name(s)

        catg = Category.query.filter_by(cat_name=s).first()
        
        if catg:
            return render_template("category.html",code=code,c=1,f=1)


        catg = Category.query.all()
        if len(catg)!=0:
            catid = catg[-1].cat_id
        else:
            catid = 'CAT0000'
        catid = str(int(catid[3:])+1)
        catid = 'CAT'+'0'*(4-len(catid))+catid
        
        catg = Category()
        catg.cat_id = catid
        catg.cat_name = s
        db.session.add(catg)
        db.session.commit()

        return redirect("/Manager/"+code+"/Dashboard")
        


# Delete Category
@app.route("/Manager/<string:code>/Category/Delete",methods=["GET", "POST"])
def delete_category(code):
    if not match(code,4):
        return redirect("/unknown")
    
    if request.method == "GET":  
        catgs = Category.query.all()
        return render_template("category.html",code=code,c=0,catgs=catgs)

    if request.method == "POST":
        id = request.form["cid"]
        items = Item.query.filter_by(cat_id=id).all()
        for i in items:
            db.session.delete(i)
        cat = Category.query.filter_by(cat_id=id).first()
        db.session.delete(cat)
        db.session.commit()

        return redirect("/Manager/"+code+"/Inventory")



# Rename Category
@app.route("/Manager/<string:code>/Category/Rename",methods=["GET", "POST"])
def rename_category(code):
    if not match(code,4):
        return redirect("/unknown")
    catgs = Category.query.all()

    if request.method == "GET":
        return render_template("category.html",code=code,c=2,catgs=catgs)

    if request.method == "POST":
        id = request.form["cid"]
        s = request.form["cname"]
        s = name(s)
        print(s)
        catg = Category.query.filter_by(cat_name=s).first()
        
        if catg:
            return render_template("category.html",code=code,c=2,f=1,catgs=catgs)
        
        cat = Category.query.filter_by(cat_id=id).first()
        cat.cat_name = s
        db.session.add(cat)

        items = Item.query.filter_by(cat_id=id).all()
        for i in items:
            i.cat_name = s
            db.session.add(i)
        db.session.commit()

        return redirect("/Manager/"+code+"/Inventory")



# Summary
@app.route("/Manager/<string:code>/Summary",methods=["GET", "POST"])
def summary(code):
    if not match(code,4):
        return redirect("/unknown")

    sell = Sell.query.all()
    dictn, l = top_sell(sell)

    data, labels = list(dictn.values()), list(dictn.keys())

    fig, ax = plt.subplots(figsize =(10, 5))
    ax.pie(data, labels = labels, autopct='%1.1f%%', startangle = 35)
    plt.legend(title ="Category", loc ="upper right", bbox_to_anchor =(1, 0.1, 0.7, 1))
    plt.savefig('static\pic.jpg')
    
    return render_template("summary.html",code=code,l=l)



# Profile
@app.route("/Manager/<string:code>/Profile",methods=["GET", "POST"])
def view_Profile(code):
    if not match(code,4):
        return redirect("/unknown")
    
    man = Manager.query.filter_by(m_id=code[:4]).first()
    if request.method == "GET":  
        return render_template("details.html",code=code,person=man,u=1,e=0)
    


# Update profile
@app.route("/Manager/<string:code>/Profile/update",methods=["GET", "POST"])
def update_Profile(code):
    if not match(code,4):
        return redirect("/unknown")
    
    person = Manager.query.filter_by(m_id=code[:4]).first ()
    if request.method == "GET":  
        return render_template("details.html",code=code,person=person,u=1,e=1)
    
    if request.method == "POST":  
        person.password = request.form['fpass']
        db.session.add(person)
        db.session.commit()
        code = person.m_id+encode(request.form['fpass'])
        return redirect("/Manager/"+code+"/Profile")










