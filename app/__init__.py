
from http import HTTPStatus
from multiprocessing.spawn import prepare
import re
import typing
from flask import Flask, jsonify, request
from csv import DictReader, DictWriter

from jinja2 import Undefined

app = Flask(__name__)

FILEPATH = 'data/products.csv'

@app.get('/products')
def get_products():
    with open(FILEPATH, 'r') as csv_file:
        reader = list(DictReader(csv_file))
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 3))
    paginated = reader[(page - 1) * per_page:per_page  * page] 
    return jsonify(paginated),200

@app.get('/products/<product_id>')
def get_by_id(product_id):
    with open(FILEPATH, 'r') as csv_file:
        reader = DictReader(csv_file)
        events = [event for event in reader if event['id'] == product_id]
        if(len(events) > 0):
            return jsonify(events),200
        return f'O item de id: {product_id} não é adequado',404
            
@app.post('/products')
def post_product():
    data = request.get_json()
    with open(FILEPATH, 'r') as csv_file:
        reader = list(DictReader(csv_file))
        last_id = int(reader[-1]["id"])
        data['id'] = last_id+1
    with open(FILEPATH, 'a') as csv_file:
        fieldnames = ['id', 'name','price']
        writer = DictWriter(csv_file, fieldnames)
        writer.writerow(dict(data))
    return "sucesso"

@app.patch('/products/<int:product_id>')
def patch_product(product_id):
    with open(FILEPATH, 'r') as csv_file:
        reader = list(DictReader(csv_file))
        teste = [test for test in reader if int(test['id']) == product_id]
        if teste == []:
            return 'id invalido',404
    with open(FILEPATH, 'w') as csv_file:
        teste = request.get_json()
        for i in reader:
            if int(i['id']) == product_id: 
                for j in i.keys():
                    if j != 'id': 
                        reader[product_id -1][j] = teste[j]
        fieldnames = ['id', 'name', 'price']
        writer = DictWriter(csv_file, fieldnames)
        writer.writeheader()
        writer.writerows(reader)
    return 'Evento atualizado',200
        
@app.delete('/products/<product_id>')
def deleteProduct(product_id):    
    with open(FILEPATH, 'r') as csv_file:
        reader = list(DictReader(csv_file))
        verify = [verify for verify in reader if verify['id'] == product_id]
        if verify == []:
            return 'id invalido',404
        event = [event for event in reader if event['id'] != product_id]
    with open(FILEPATH, 'w') as csv_file:
        fieldnames = ['id', 'name', 'price']
        writer = DictWriter(csv_file, fieldnames)
        writer.writeheader()
        writer.writerows(event)
    return 'Evento deletado',200
 