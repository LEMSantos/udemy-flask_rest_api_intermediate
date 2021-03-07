from flask_restful import Resource, reqparse
from http import HTTPStatus
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        required=True,
        help='This field cannot be blank.'
    )
    parser.add_argument(
        'password',
        required=True,
        help='This field cannot be blank.'
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data.get('username')):
            return {
                'message': f'A user with that username already exists.'
            }, HTTPStatus.BAD_REQUEST

        user = UserModel(**data)
        user.save()

        return {
            'message': 'User created successfully.',
        }, HTTPStatus.CREATED
