from flask import Flask, redirect, url_for, request, render_template
#render template es para las plantillas de html

from pymongo import MongoClient
import pprint

from bson import ObjectId

client=MongoClient('mongodb://localhost:27017/')
db=client.Joyeria #nombre de la base de datos que hay que crear
categorys=db.categorias
products=db.productos
cart=list()

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products/<category>')
def show_products(category):
    #print(type(category))
    id_category=categorys.find_one({'nombre':category},{'nombre':0})
    #pprint.pprint(id_category)#{'_id': 1}
    #print(type(id_category))#<class 'dict'>
    #print(id_category['_id'])#1
    list_products=products.find({'id_categoria':id_category['_id']})
    #print(type(list_products))
    #for prod in list_products:
     #   print(prod.imagen)
    return render_template('products.html',category=category,products=list_products)

@app.route('/adminview')
def administrator_view():
    list_products=products.aggregate([{
    "$lookup": {
    "from": 'categorias',
    "localField": 'id_categoria',
    "foreignField": '_id',
    "as": 'categoria'}},
    {"$unwind":'$categoria'}])
    print(type(list_products))
    return render_template("admin_view.html",products=list_products)

@app.route('/removeproduct')
def removeproduct():
    str_id_prod = request.values.get('_id')
    id_prod=int(str_id_prod)
    print(type(id_prod))
    products.delete_one({'_id': id_prod})
    return redirect('/adminview')

@app.route('/updateproduct')
def updateproduct():
    str_id_prod = request.values.get('_id')
    id_prod=int(str_id_prod)
    product_to_update=products.aggregate([{
    "$lookup": {
    "from": 'categorias',
    "localField": 'id_categoria',
    "foreignField": '_id',
    "as": 'categoria'}},
    {"$unwind":'$categoria'},
    {"$match":{'_id':id_prod}}])
    for eachproduct in product_to_update:
        product=eachproduct
    return render_template('update_one_product.html',product=product)

@app.route('/update_one_product', methods=["POST"])
def update_one_product():
    str_id_prod = request.form["id"]
    id_prod=int(str_id_prod)
    nombre = request.form["nombre"]
    categoria = request.form["categoria"]
    obj_id_categoria=categorys.find_one({'nombre':categoria})
    id_categoria=obj_id_categoria['_id']
    str_precio = request.form["precio"]
    precio=int(str_precio)
    imagen = request.form["imagen"]
    str_contador_vistas = request.form["contador_vistas"]
    contador_vistas=int(str_contador_vistas)
    cant = request.form["cant"]
    products.update({'_id':id_prod},{"$set":{'nombre':nombre,'id_categoria':id_categoria,'precio':precio,'imagen':imagen,'contador_vistas':contador_vistas}})
    return redirect('/adminview')

@app.route('/detail/<product_name>')
def product_detail(product_name):
    product=products.find_one_and_update({'nombre':product_name},{"$inc":{'contador_vistas':1}})
    return render_template('product_detail.html',product=product)

@app.route('/add_to_cart', methods=["POST"])
def add_to_cart():
    string_cant = request.form["cant"]
    cant=int(string_cant)
    string_id_prod = request.form["id"]
    id_prod=int(string_id_prod)
    #Encontrando el producto que se quiere comprar
    product=products.find_one({'_id':id_prod})
    #print(product,' ',type(product))
    #Enlazandolo con la cantidad que se quiere comprar del producto
    d1={'cant_sale':cant}
    d2={'subtotal':cant*float(product['precio'])}
    product.update(d1)
    product.update(d2)
    #print(product,' ',type(product))
    redirect_string='/detail/'+product['nombre']
    print(cant)
    #print(dic1[product])
    print(id_prod)
    cart.append(product)
    return render_template('product_detail.html',product=product)

@app.route('/my_cart')
def show_cart():
    total=0
    for product in cart:
        total=total+float(product['precio'])*float(product['cant_sale'])
    print(cart)
    print(total)
    return render_template('my_cart.html',cart=cart,total=total)

if __name__ == '__main__':
    app.run(debug=True) #debug=true para no tener que estar lanzando a cada rato el localhost

#pulsar ctrl + shift + R para recargar la pagina sin cache 