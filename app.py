from flask import Flask, jsonify, make_response, request
import requests
from pymongo import MongoClient
import os

from bson.objectid import ObjectId
app = Flask(__name__)

cf_port = os.getenv("PORT")

client = MongoClient("mongodb://localhost:27017/restaurants")

db = client.restaurants                             #Select the database
coll = db.menu_collection


@app.route("/add",methods=['POST'])  #create
def add():
    data = request.get_json()

    new_dish={'Dish': data['Dish'],
              'Category': data['Category'],
              'Price': data['Price']
              }
    coll.insert_one(new_dish)
    return  jsonify({'message':'dish added successfully'})

@app.route("/getall", methods= ['GET'])    #read
def read_all():
    menu = coll.find()
    out=[]
    for dish in menu:
        menu_data ={}
        menu_data["_id"] = str(dish["_id"])
        menu_data["Dish"] = dish["Dish"]
        menu_data["Category"] = dish["Category"]
        menu_data["Price"] = dish["Price"]
        out.append(menu_data)
    return jsonify({"data": out})

@app.route("/get/<id>", methods = ['GET'])   #read by id
def get_one(id):
    dish = coll.find_one({"_id": ObjectId(id)})
    if dish:
        menu_data = {}
        menu_data["_id"] = str(dish["_id"])
        menu_data["Dish"] = dish["Dish"]
        menu_data["Category"] = dish["Category"]
        menu_data["Price"] = dish["Price"]
        return jsonify({"data":menu_data})
    # elif(ObjectId(id).is_valid()==False or not dish):
    #     return jsonify({"data":"no dish found"})

@app.route("/update/<id>", methods= ['POST'])  #update
def update_one(id):
     menu = coll.find_one({"_id": ObjectId(id)})

     if menu :
         data = request.get_json()

         new_dish = {'Dish': data['Dish'],
                     'Category': data['Category'],
                     'Price': data['Price']
                     }


         updated_menu = coll.update_one({"_id": ObjectId(id)}, {"$set": new_dish})
         if updated_menu:
             return jsonify({'message':'menu updated'})
         else:
            return jsonify({'message':'not updated'})


@app.route("/delete/<id>", methods= ['DELETE']) #delete
def delete_dish(id):
    menu = coll.find_one({"_id": ObjectId(id)})
    if menu:
        coll.delete_one({"_id": ObjectId(id)})
        return jsonify({'message':'dish deleted successfully'})
    else:
        return jsonify({'message':'dish not present'})






if __name__ == '__main__':
   if cf_port is None:
       app.run(host='127.0.0.1', port=5000, debug=True)
   else:
       app.run(host='127.0.0.1', port=int(cf_port), debug=True)


