from flask import Blueprint,jsonify,request,current_app
from pydantic import ValidationError
from app.models.user import LoginPayload
from bson import ObjectId
from datetime import datetime,timedelta,timezone
import jwt
import os
import csv
import io
from app import db
from app.decorators import token_required
from app.models.product import *
from app.models.sales import Sales


main_bp = Blueprint('main_bp',__name__)

# RF: O sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data) 

    except ValidationError as e:
        return jsonify({"error": e.errors()}),400
    except Exception as e:
        return jsonify({"error": 'Erro durante a requisição do dado'}),500
    
    
    if user_data.name == 'admin' and user_data.password == 'supersecret':
        token = jwt.encode({
            'user_id' : user_data.name,
            'exp' : datetime.now(timezone.utc) + timedelta(minutes= 30)

        },current_app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'access_token': token}),200
    
    return jsonify({"message": "Credenciais invalidas!"})   

    
    

# RF: O sistema deve permitir listagem de todos os produtos
@main_bp.route('/products', methods=['GET'])
def get_products():
    products_cursor = db.products.find({})
    products_list = [ProductDbModel(**product).model_dump(by_alias=True,exclude_none=True) for product in products_cursor]

    return jsonify(products_list)

# RF: O sistema deve permitir a criacao de um novo produto
@main_bp.route('/products', methods=['POST'])
@token_required
def create_product(token):
    try:
        product = Product(**request.get_json())
    except ValidationError as e:
        return jsonify({"Error": e.errors()})
    
    result = db.products.insert_one(product.model_dump())

    return jsonify({"message":"Esta é a rota de criação de produto",
                    "id":str(result.inserted_id)}),201

# RF: O sistema deve permitir a visualizacao dos detalhes de um unico produto
@main_bp.route('/products/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({'Erro': f'Erro ao transformar o {product_id} em ObjectId: {e}'})
    
    product = db.products.find_one({'_id' : oid})
    if product:
        product_model = ProductDbModel(**product).model_dump(by_alias=True,exclude_none=True)
        return jsonify(product_model)
    else:
        return jsonify({'Erro': f'Erro achar produto com id {product_id} no banco de dados.'})

# RF: O sistema deve permitir a atualizacao de um unico produto e produto existente
@main_bp.route('/product/<string:product_id>', methods=['PUT'])
@token_required
def update_products(token,product_id):
    try:
        oid = ObjectId(product_id)
        update_data = UpdateProduct(**request.get_json())
    except ValidationError as e:
        return jsonify({"Error": e.errors()})

    upadate_result = db.products.update_one(
        {"_id":oid},
        {"$set": update_data.model_dump(exclude_unset=True)}
        )
    
    if upadate_result.matched_count == 0:
        return jsonify({"Error": f"Produto com id {oid} não encontrado."}),500
    
    update_product = db.products.find_one({"_id":oid})
    return jsonify(ProductDbModel(**update_product).model_dump(by_alias=True,exclude=None))

# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route('/product/<string:product_id>', methods=['DELETE'])
@token_required
def delete_product(token,product_id):
    try:
        oid = ObjectId(product_id)
    except Exception as e:
        return jsonify({"Error": "Id do produto errado"}),400
    
    delete_result = db.products.delete_one({"_id":oid})
    if delete_result.deleted_count == 0:
        return jsonify({"Error": f"Produto com id {oid} não encontrado"}),404

    return "",200

# RF: O sistema deve permitir a importacao de vendas através de um arquivo
@main_bp.route('/sales/upload', methods=['POST'])
@token_required
def upload_sales(token):
    if 'file' not in request.files:
        return jsonify({'Erro':'Nenhum arquivo enviado'}),400

    file = request.files['file']

    if file.name == '':
        return jsonify({'Erro':'Nenhum arquivo selecionado'}),400
    
    if file and file.name.endswith('.csv'):
        csv_stream = io.StringIO(file.stream.read().decode('UTF-8'),newline=None)
        csv_reader = csv.DictReader(csv_stream)

        files_to_insert = []
        errors = []

        for row_number,row in enumerate(csv_reader,1):
            try:
                sale_data = Sales(**row)
                files_to_insert.append(sale_data.model_dump())
            except ValidationError as e:
                errors.append(f"Linha {row_number}: Dados inválidos - {e.errors()}")
            except Exception as e:
                errors.append(f"Linha {row_number}: Erro inesperado - {str(e)}")
            
        if files_to_insert:
            try:
                db.sales.insert_many(files_to_insert)
            except Exception as e:
                return jsonify({"error": f"Erro no BD: {str(e)}"}), 500
        
        return jsonify({
            "message": "Upload processado com sucesso.",
            "vendas_importadas": len(files_to_insert),
            "erros_encontrados": errors
        }), 200
    
@main_bp.route('/')
def index():
    return jsonify({'message':'Bem vindo ao Stylesync!'})



