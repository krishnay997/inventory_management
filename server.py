import peeweedbevolve # new; must be imported before models
from flask import Flask, render_template, request,redirect
from models import db, Store, Warehouse


app = Flask(__name__)

@app.before_request
def before_request():
   db.connect()

@app.after_request
def after_request(response):
   db.close()
   return response

@app.cli.command() # new
def migrate(): # new 
   db.evolve(ignore_tables={'base_model'}) # new

@app.route("/")
def index():
   return render_template('index.html')

@app.route("/store")
def store():
   return render_template('store.html')

@app.route("/store", methods=["POST"])
def store_add():
   Store.create(name=request.form.get("store_name"))
   return redirect("/store")

@app.route("/warehouse")
def warehouse(): 
   store = Store.select()
   return render_template('warehouse.html',store=store)

@app.route("/warehouse", methods=["POST"])
def warehouse_add():
   print(request.form["store_id"]) 
   store = Store.get_by_id(request.form["store_id"])
   Warehouse.create(location=request.form.get("warehouse_location"),store=store)
   return redirect("/warehouse")

if __name__ == '__main__':
   app.run()