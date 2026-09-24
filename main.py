import os

from uuid import uuid4
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pymongo import MongoClient

MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017/')

app = FastAPI(
    title='User API',
    description='User API with FastAPI and MongoDB',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


class User(BaseModel):
    name: str
    password: str

    admin: bool = False


client = MongoClient(MONGO_URL)
db = client['user']['production']


def find_user(user_id: str):
    document = db.find_one({'_id': user_id})

    if not document:
        raise HTTPException(status_code=404, detail=f'user \'{user_id}\' not found')

    return document


def insert_user(name: str, password: str, admin: bool):
    user_id = str(uuid4())

    db.insert_one({
        '_id': user_id,

        'name': name,
        'password': password,

        'admin': admin
    })

    return user_id


# user create


@app.post(
    '/user',
    description='Creates a new user with the provided name, password, and admin status.',
    response_description='Returns a success message upon creation.',
)
async def create_user(user: User):
    user_id = insert_user(user.name, user.password, user.admin)

    return {'message': f'created: {user_id}', 'id': user_id}


# user read


@app.get(
    '/user/{user_id}',
    description='Retrieves a user\'s with the specified ID.',
    response_description='Returns the user information if found, or 404 if the user was not found.',
)
async def read_user(user_id: str):
    return find_user(user_id)


# user update


@app.put(
    '/user/{user_id}',
    description='Updates the information of an existing user with the specified ID.',
    response_description='Returns a success message upon updating, or 404 if the user was not found.'
)
async def update_user(user_id: str, user: User):
    find_user(user_id)

    db.update_one({'_id': user_id}, {'$set': user.model_dump()})

    return {'message': f'updated: {user_id}'}


# user delete


@app.delete(
    '/user/{user_id}',
    description='Deletes a user with the specified ID.',
    response_description='Returns a success message upon deletion, or 404 if the user was not found.'
)
async def delete_user(user_id: str):
    find_user(user_id)

    db.delete_one({'_id': user_id})

    return {'message': f'deleted: {user_id}'}


# users search


@app.get(
    '/users/',
    description='Retrieves a list of all users.',
    response_description='Returns the list of users (empty if there are none).'
)
async def read_users():
    return list(db.find())


# register


@app.post(
    '/register',
    description='Creates a new user with the provided name, password.',
    response_description='Returns a success message upon creation.',
)
async def register(user: User):
    user_id = insert_user(user.name, user.password, False)

    return {'message': f'created: {user_id}', 'id': user_id}


# login


@app.post(
    '/login',
    description='Validates user credentials \'name and password\' against the database.',
    response_description='Returns the user ID if the login is successful, or 401 if the login is invalid.'
)
async def login(name: str, password: str):
    document = db.find_one({'name': name, 'password': password})

    if not document:
        raise HTTPException(status_code=401, detail='invalid login')

    return document['_id']
