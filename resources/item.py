from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from http import HTTPStatus
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank!',
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help='Every item needs a store id.'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            return {'data': item.json()}

        return {'message': 'Item not found'}, HTTPStatus.NOT_FOUND

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {
                'message': f"An item with name '{name}' already exists",
            }, HTTPStatus.BAD_REQUEST

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save()
        except:
            return {
                'message': 'An error occurred inserting the item.'
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {'data': item.json()}, HTTPStatus.CREATED

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data.get('price')

        item.save()

        return {'data': item.json()}


class ItemList(Resource):

    def get(self):
        return {
            'data': [item.json() for item in ItemModel.query.all()],
        }
