from flask import Flask, render_template, request, redirect, url_for
import pymongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
cliente = pymongo.MongoClient("mongodb://localhost:27017")
db = cliente['blog']

@app.route("/")
def listado():
    entradas = db['entrada']
    resultado = entradas.find().sort("fecha", -1)
    salida = []
    for x in resultado:
        salida.append(x)

    return render_template("listado.html", blog=salida)

@app.route("/entrada/<string:id>", methods=['GET'])
def entrada(id):
    entradas = db['entrada']
    info = entradas.find_one({"_id": ObjectId(id)})
    return render_template("entrada.html", entrada=info)

@app.route("/nueva", methods=['GET'])
def nueva():
    return render_template("formulario.html")

@app.route("/nueva", methods=['POST'])
def guardar_alumno():
    titulo = request.form['titulo']
    descripcion = request.form['descripcion']
    contenido = request.form['contenido']
    usuario = request.form['usuario']

    entradas = db['entrada']
    nueva_entrada = {"titulo": titulo, "descripcion": descripcion, "contenido":contenido, "usuario":usuario, "fecha":datetime.now()}
    entradas.insert_one(nueva_entrada)

    return redirect(url_for('listado'))

app.run()