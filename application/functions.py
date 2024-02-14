from flask import render_template, request, redirect
from flask import current_app as app
from application.model import *
import datetime as d
import string





# checking for valid person
def match(code,n):
    if n==4:
        person = Manager.query.filter_by(m_id = code[:n]).first()
    elif n==5:
        person = Customer.query.filter_by(c_id = code[:n]).first()
    if not person:
        return False
    if code[n:] != encode(person.password):
        return False
    return True


# encode password
def encode(password):
    up = list(string.ascii_uppercase)
    lw = list(string.ascii_lowercase)
    di = list(string.digits)
    sp = list(string.punctuation)
    uplw = string.ascii_uppercase + string.ascii_lowercase

    new = ""
    for p in password:
        if p in up:
            new += lw[(up.index(p) + 11)%26]

        elif p in lw:
            new += di[(lw.index(p) + 7)%10]
        
        elif p in di:
            new += uplw[(di.index(p) + 13)%17]
        
        elif p in sp:
            new += uplw[(sp.index(p) + 29)%43]
        
        else:
            new += "x"
    return new


# extract items
def find_items(q=None):
    items = Item.query.all()
    dictn = {}
    if q==None:
        for i in items:
            x = i.cat_name
            if x not in dictn:
                dictn[x] = [i]
            else:
                dictn[x].append(i)
    else:
        for i in items:
            x = i.i_name
            if q.lower() in x.lower():
                x = i.cat_name
                if x not in dictn:
                    dictn[x] = [i]
                else:
                    dictn[x].append(i)
    return dictn


def find_items2(q=None):
    items = Item.query.all()
    dictn = {}
    if q==None:
        for i in items:
            if i.exp_date >= i.mfg_date:
                x = i.cat_name
                if x not in dictn:
                    dictn[x] = [i]
                else:
                    dictn[x].append(i)
    else:
        for i in items:
            x = i.i_name
            if i.exp_date >= i.mfg_date and q.lower() in x.lower():
                x = i.cat_name
                if x not in dictn:
                    dictn[x] = [i]
                else:
                    dictn[x].append(i)
    return dictn


# extract items
def find_items3(q):
    items = Item.query.all()
    cat = Category.query.all()
    dictn = {}

    for i in items:
        if q.lower() in i.cat_name.lower():
            x = i.cat_name
            if x not in dictn:
                dictn[x] = [i]
            else:
                dictn[x].append(i)
    return dictn


# convert category name
def name(s):
    s = s.strip()
    l = s.split(" ")
    s = ""
    for i in l:
        if i.isalpha():
            s = s + i[0].upper() + i[1:].lower() + " "
        else:
            s = s + i + " "
    s = s.strip()

    return s


# extract top selling item
def top_sell(sell):
    sell = Sell.query.all()
    dictn, dictn2 = {}, {}
    for s in sell:
        if s.cat_name not in dictn:
            dictn[s.cat_name] = s.profit
        else:
            dictn[s.cat_name] += s.profit
        
        if s.i_name not in dictn2:
            dictn2[s.i_name] = [s.cat_name, s.selling_quantity]
        else:
            dictn2[s.i_name][1] += s.selling_quantity

    x=list(dictn2.values())
    x = sorted(x, key=lambda z:z[1],reverse=True)
    s, c = [], 0
    for i in x:
        if i[1] not in s:
            s.append(i[1])
            c += 1
            if c==5:
                break
    d=[]
    for i in s:
        for j in dictn2.keys():
            if(dictn2[j][1] == i):
                d.append([j,dictn2[j][0]]) 
    
    return dictn, d


