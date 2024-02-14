from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()



class Manager(db.Model):
    __tablename__ = 'manager'
    m_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String)
    gender = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


class Customer(db.Model):
    __tablename__ = 'customer'
    c_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String)
    gender = db.Column(db.String, nullable=False)
    dob = db.Column(db.String, nullable=False)
    mobile = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    no_purchase = db.Column(db.Integer, nullable=False)


class Category(db.Model):
    __tablename__ = 'category'
    cat_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    cat_name = db.Column(db.String, unique=True, nullable=False)


class Item(db.Model):
    __tablename__ = 'item'
    i_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    i_name = db.Column(db.String, nullable=False)
    cat_id = db.Column(db.String, db.ForeignKey("category.cat_id"), nullable=False)
    cat_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    mfg_date = db.Column(db.String, nullable=False)
    exp_date = db.Column(db.String, nullable=False)


class Sell(db.Model):
    __tablename__ = 'sell'
    s_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    c_id = db.Column(db.String, db.ForeignKey("customer.c_id"), nullable=False)
    cat_id = db.Column(db.String, nullable=False)
    cat_name = db.Column(db.String, nullable=False)
    i_id = db.Column(db.String, nullable=False)
    i_name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    selling_quantity = db.Column(db.Integer, nullable=False)
    profit = db.Column(db.Integer, nullable=False)

