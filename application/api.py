from flask import make_response
from flask_restful import Resource, fields, marshal_with, reqparse
from werkzeug.exceptions import HTTPException
import json
import datetime as d
from application.model import *
from application.functions import *



# ----------- Exception Handling -----------
class FoundError(HTTPException):
    def __init__(self, status_code, message=''):
        self.response = make_response(message, status_code)

class NotGivenError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code": error_code, "error_message": error_message}
        self.response = make_response(json.dumps(message), status_code)



# ----------- Output Feilds -----------
item_details = {
    "i_id": fields.String,
    "i_name": fields.String,
    "cat_name": fields.String,
    "quantity": fields.Integer,
    "unit": fields.String,
    "price": fields.Integer,
    "stock": fields.Integer,
    "mfg_date": fields.String,
    "exp_date": fields.String
}

category_details = {
    "cat_id": fields.String,
    "cat_name": fields.String
}
category_details2 = {
    "cat_id": fields.String,
    "cat_name": fields.String,
    "item_list": fields.List
}



# ----------- Parsers -----------
item_edit = reqparse.RequestParser()
item_edit.add_argument("price")
item_edit.add_argument("stock")

item_info = reqparse.RequestParser()
item_info.add_argument("i_name")
item_info.add_argument("cat_name")
item_info.add_argument("quantity")
item_info.add_argument("unit")
item_info.add_argument("price")
item_info.add_argument("stock")
item_info.add_argument("mfg_date")
item_info.add_argument("exp_date")

cat_info = reqparse.RequestParser()
cat_info.add_argument("cat_name")



# ----------- APIs -----------
class ItemAPI(Resource):

    # get item details
    @marshal_with(item_details)
    def get(self, item_id):
        item = Item.query.filter_by(i_id=item_id).first()

        if item:
            return item
        else:
            raise FoundError(status_code=404)
    

    # upadate item price and stock
    @marshal_with(item_details)
    def put(self, item_id):
        item = Item.query.filter_by(i_id=item_id).first()

        if item is None:
            raise FoundError(status_code=404)
        
        args = item_edit.parse_args()
        price = args.get("price", None)
        stock = args.get("stock", None)

        if price is None and stock is None:
            raise NotGivenError(status_code=400, error_code="I009", error_message="price and stock both cannot be empty")
        else:
            if price is None:
                item.stock = stock
            elif stock is None:
                item.price = price
            else:
                item.price = price
                item.stock = stock
            db.session.add(item)
            db.session.commit()
        
            return item


    # delete item
    def delete(self, item_id):
        item = Item.query.filter_by(i_id=item_id).first()

        if item is None:
            raise FoundError(status_code=404)

        db.session.delete(item)
        db.session.commit()
        return "", 200


    # add item
    @marshal_with(item_details)
    def post(self):
        args = item_info.parse_args()
        i_name = args.get("i_name", None)
        cat_name = args.get("cat_name", None)
        quantity = args.get("quantity", None)
        unit = args.get("unit", None)
        price = args.get("price", None)
        stock = args.get("stock", None)
        mfg_date = args.get("mfg_date", None)
        exp_date = args.get("exp_date", None)

        if i_name is None:
            raise NotGivenError(status_code=400, error_code="I001", error_message="item name is required")
        if cat_name is None:
            raise NotGivenError(status_code=400, error_code="C001", error_message="category name is required")
        if quantity is None:
            raise NotGivenError(status_code=400, error_code="I002", error_message="quantity is required")
        if unit is None:
            raise NotGivenError(status_code=400, error_code="I003", error_message="unit is required")
        if price is None:
            raise NotGivenError(status_code=400, error_code="I004", error_message="price is required")
        if stock is None:
            raise NotGivenError(status_code=400, error_code="I005", error_message="stock is required")
        if mfg_date is None:
            raise NotGivenError(status_code=400, error_code="I006", error_message="mfg_date is required")
        if exp_date is None:
            raise NotGivenError(status_code=400, error_code="I007", error_message="exp_date is required")
        
        d1 = d.datetime.strptime(mfg_date, '%Y-%m-%d').date()
        d2 = d.datetime.strptime(exp_date, '%Y-%m-%d').date()
        if d1>d2:
            raise NotGivenError(status_code=400, error_code="I008", error_message="mfg_date cannot greater than exp date")

        cat = Category.query.filter_by(cat_name=cat_name).first()
        if cat is None:
            raise NotGivenError(status_code=400, error_code="C002", error_message="category name is not present")


        its = Item.query.all()
        if len(its)!=0:
            iid = its[-1].i_id
        else:
            iid = 'C0000'
        iid = str(int(iid[1:])+1)
        iid = 'I'+'0'*(5-len(iid))+iid

        item = Item()
        item.i_id = iid
        item.i_name = i_name
        item.cat_id = cat.cat_id
        item.cat_name = cat_name
        item.quantity = quantity
        item.unit = unit
        item.price = price
        item.stock = stock
        item.mfg_date = mfg_date
        item.exp_date = exp_date

        db.session.add(item)
        db.session.commit()
        
        return item, 201





class CategoryAPI(Resource):

    # get item details
    def get(self, cat_id):
        cat = Category.query.filter_by(cat_id=cat_id).first()
        if cat:
            its = Item.query.filter_by(cat_id=cat_id).all()
            itemList=[]
            for i in its:
                itemList.append(i.i_name)
            return {"cat_id": cat_id, "cat_name": cat.cat_name, "item list": itemList}
        else:
            raise FoundError(status_code=404)
    

    # delete category
    def delete(self, cat_id):
        cat = Category.query.filter_by(cat_id=cat_id).first()

        if cat is None:
            raise FoundError(status_code=404)

        items = Item.query.filter_by(cat_id=cat_id).all()
        for i in items:
            db.session.delete(i)

        db.session.delete(cat)
        db.session.commit()
        return "", 200


    # add category
    @marshal_with(category_details)
    def post(self):
        args = cat_info.parse_args()
        cat_name = args.get("cat_name", None)

        if cat_name is None:
            raise NotGivenError(status_code=400, error_code="C001", error_message="category name is required")

        cat_name = name(cat_name)
        catg = Category.query.filter_by(cat_name=cat_name).first()
        if catg:
            raise NotGivenError(status_code=400, error_code="C001", error_message="category name already exists")


        catg = Category.query.all()
        if len(catg)!=0:
            catid = catg[-1].cat_id
        else:
            catid = 'CAT0000'
        catid = str(int(catid[3:])+1)
        catid = 'CAT'+'0'*(4-len(catid))+catid
        
        catg = Category()
        catg.cat_id = catid
        catg.cat_name = cat_name
        db.session.add(catg)
        db.session.commit()
        
        return catg, 201




