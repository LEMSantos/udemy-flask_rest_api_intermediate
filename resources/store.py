from flask_restful import Resource
from http import HTTPStatus
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return {'data': store.json()}

        return {'message': 'Store not found'}, HTTPStatus.NOT_FOUND

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {
                'message': f"An store with name '{name}' already exists.",
            }, HTTPStatus.BAD_REQUEST

        store = StoreModel(name)

        try:
            store.save()
        except:
            return {
                'message': 'An error occurred creating the store.'
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return {'data': store.json()}, HTTPStatus.CREATED

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete()

        return {'message': 'Store deleted.'}


class StoreList(Resource):

    def get(self):
        return {
            'data': [store.json() for store in StoreModel.find_all()],
        }
