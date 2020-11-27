from flask import Flask, redirect, url_for, request, render_template
#render template es para las plantillas de html

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product')
def show_products():
    return 'Products'

if __name__ == '__main__':
    app.run(debug=True) #debug=true para no tener que estar lanzando a cada rato el localhost

#pulsar ctrl + shift + R para recargar la pagina sin cache 