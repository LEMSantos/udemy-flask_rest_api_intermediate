from flask_restful import Resource, reqparse
from http import HTTPStatus
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from models.user import UserModel
from blocklist import BLOCKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    required=True,
    help='This field cannot be blank.'
)
_user_parser.add_argument(
    'password',
    required=True,
    help='This field cannot be blank.'
)

class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data.get('username')):
            return {
                'message': f'A user with that username already exists.'
            }, HTTPStatus.BAD_REQUEST

        user = UserModel(**data)
        user.save()

        return {
            'message': 'User created successfully.',
        }, HTTPStatus.CREATED


class User(Resource):

    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        return {'data': user.json()}

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        user.delete()

        return {'message': 'User deleted.'},


class UserLogin(Resource):

    def post(self):
        data = _user_parser.parse_args()
        username = data.get('username')
        password = data.get('password')

        user = UserModel.find_by_username(username)

        if user and safe_str_cmp(user.password, password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }

        return {'message': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jti = get_jwt().get('jti')
        BLOCKLIST.add(jti)

        return {'message': 'Successfully logged out.'}


class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, fresh=False)

        return {
            'access_token': access_token,
        }
