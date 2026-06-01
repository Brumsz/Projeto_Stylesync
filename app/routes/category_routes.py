from flask import Blueprint ,request,jsonify
from pydantic import ValidationError
from bson import ObjectId
from app.models.category import *
from app import db
from app.decorators import token_required


category_bp = Blueprint('category_bp',__name__,url_prefix='/categorys')

#lista todas as categorias
@category_bp.route('/all', methods=['GET'])
def get_categorys():
    category_cursor = db.category.find({})
    category_list = [CategoryDBModel(**category).model_dump(by_alias=True,exclude_none=True)for category in category_cursor]
    return jsonify(category_list)

#lista uma categoria pelo id
@category_bp.route('/<string:category_id>', methods=['GET'])
def get_categorys_products(category_id:str):
    try:    
        oid = ObjectId(category_id)
    except Exception as e:
        return jsonify({'Erro': f'Erro ao transformar o {category_id} em ObjectId: {e}'})

    category_find = db.category.find_one({'_id' : oid})

    if category_find:
        category = CategoryDBModel(**category_find).model_dump(by_alias=True,exclude_none=True)
        return jsonify(category)
    else:
        return jsonify({'message':f'Categoria com id {category_id} não encontrada!'})

#cria uma nova categoria
@category_bp.route('/',methods=['POST'])
@token_required
def create_category(token):
    try:
        raw_data = request.get_json()
        user_data = Category(**raw_data)
        
        return jsonify({'message': f'A categoria {user_data.name} foi cadastrada com sucesso!'})

    except ValidationError as e:
        return jsonify({'error':e.errors()}),400
    
    except Exception as e:
        return jsonify({'error':"Erro durante a requisição do dado"}),500

@category_bp.route('/<string:category_id>', methods=['DELETE'])
@token_required
def delete_category(token,category_id):
    try:
        oid = ObjectId(category_id)
    except Exception as e:
        return jsonify({"Error": "Id esta errado"}),400
    
    category_delete = db.category.delete_one({"_id":oid})

    if category_delete.deleted_count == 0:
        return jsonify({"Error": f"categoria com id {category_id} não encontrada"}),400

    return "",200