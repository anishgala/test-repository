# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 20:06:50 2021

@author: abc
"""
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#Definiing our resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
    )
    
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json(), 201
    

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            
        return {'message': 'Item deleted'}
    
    
    def put(self, name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
       
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            
        item.save_to_db()
        
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}