from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///purchase_order2.db")
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    product = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# with app.app_context():
#     db.create_all()

class MyForm(FlaskForm):
    name = StringField("姓名", validators=([DataRequired()]), render_kw={"placeholder": "範例: 吳世勳"})
    email = StringField("電子郵件", validators=([DataRequired(), Email()]), render_kw={"placeholder": "範例: you@gmail.com"})
    phone = StringField("電話", validators=([DataRequired()]), render_kw={"placeholder": "範例: 0911123456"})
    product = StringField("產品", validators=([DataRequired()]), render_kw={"placeholder": "範例: 雨傘"})
    price = DecimalField("價錢", validators=([DataRequired()]), render_kw={"placeholder": "範例: 140"})
    submit = SubmitField("送出")

class InquiryForm(FlaskForm):
    email = StringField("電子郵件", validators=([DataRequired(), Email()]), render_kw={"placeholder": "範例: you@gmail.com"})
    submit = SubmitField("送出")

@app.route('/', methods=["GET", "POST"])
def home():
    name = None
    email = None
    phone = None
    product = None
    price = None
    form=MyForm()
    if form.validate_on_submit():
        order = Order(name=form.name.data, email=form.email.data, phone=form.phone.data, product=form.product.data, price=form.price.data)
        db.session.add(order)
        db.session.commit()
        
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        product = form.product.data
        price = form.price.data
        form.name.data = ""
        form.email.data = ""
        form.phone.data = ""
        form.product.data = ""
        form.price.data = ""
        flash("訂單成功送出!")
    
    all_orders = Order.query.order_by(Order.date_added)
    return render_template('home.html', form=form, name=name, email=email, phone=phone, product=product, price=price, all_orders=all_orders)

@app.route('/order', methods=["GET", "POST"])
def order():
    email = None
    form = InquiryForm()
    if form.validate_on_submit():
        email = form.email.data
        form.email.data = ""
        flash("查詢結果:")

    all_orders = Order.query.order_by(Order.date_added)
    return render_template('order.html', form=form, email=email, all_orders=all_orders)

if __name__ == "__main__":
    app.run(debug=True)