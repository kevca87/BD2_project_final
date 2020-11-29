from flask import Flask, redirect, url_for, request, render_template
#render template es para las plantillas de html

from pymongo import MongoClient
import pprint

client=MongoClient('mongodb://localhost:27017/')
db=client.Joyeria #nombre de la base de datos que hay que crear
categorys=db.categorias
products=db.productos

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products/<category>')
def show_products(category):
    print(type(category))
    id_category=categorys.find_one({'nombre':category},{'nombre':0})
    pprint.pprint(id_category)#{'_id': 1}
    print(type(id_category))#<class 'dict'>
    print(id_category['_id'])#1
    list_products=products.find({'id_categoria':id_category['_id']})
    print(type(list_products))
    #for prod in list_products:
     #   print(prod.imagen)
    return render_template('products.html',category=category,products=list_products)
    
if __name__ == '__main__':
    app.run(debug=True) #debug=true para no tener que estar lanzando a cada rato el localhost

#pulsar ctrl + shift + R para recargar la pagina sin cache 