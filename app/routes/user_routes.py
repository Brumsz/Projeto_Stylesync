from flask import Blueprint,jsonify,request
from pydantic import ValidationError
from bson import ObjectId
from app.decorators import token_required
from app.models.user import User,UserDbModel
from app import db

user_bp = Blueprint('user_bp',__name__,url_prefix='/user')

#retornara todos os usuarios sem mostrar as senhas
@user_bp.route("/all",methods = ['GET'])
@token_required
def get_users(token):
    db_request = db.users.find({})
    user_list = [UserDbModel(**user).model_dump(exclude_none=True) for user in db_request]
    return jsonify(user_list)

#criar novos usuarios
@user_bp.route("",methods=['POST'])
@token_required
def users_create(token):
    try:
        user_data = User(**request.get_json())
    except ValidationError as e:
        return jsonify({"Error":e.error()}),404
    
    user_insert = db.users.insert_one(user_data.model_dump())

    return jsonify ({"mensage":f"Usuario com id {str(user_insert.inserted_id)} foi criado"}),200
    

#deletar usuarios
@user_bp.route("/<string:user_id>",methods=['DELETE'])
@token_required
def delete_user(token,user_id):
    try:
        oid = ObjectId(user_id)
    except Exception as e:
        return jsonify({"Error": "Id do usuario esta errado"}),400
    
    user_deleted = db.users.delete_one({"_id":oid})

    if user_deleted.deleted_count == 0:
        return jsonify({"Error": f"Usuario com id {oid} não encontrado"}),404
    
    return "",200