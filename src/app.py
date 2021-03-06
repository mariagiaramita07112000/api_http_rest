import os
from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from geoalchemy2 import Geometry

app= Flask(__name__)

inmuebles ="sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
#indico donde esta la base,  metodo que proviene de la documentacion 
app.config['SQLALCHEMY_DATABASE_URI']= inmuebles
#configuracion para evitar que pase una advertencia al ejecutar el programa 
app.config['SQLAlchemy_TRACK_MODIFICATIONS']=False

#instancio
db = SQLAlchemy(app)
ma = Marshmallow(app)

#defino una clase que hereda el modelo de la base de datos
#metodo para definirla

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True )
    latitud=db.Column(db.Float, nullable=False)
    longitud=db.Column(db.Float, nullable=False)
    address= db.Column(db.String(70) ,nullable=False)
    area= db.Column(db.Float, nullable=False)
    rooms= db.Column(db.Float, nullable=False)
    garage = db.Column(db.Float)

#funcion que se ejecuta cada vez que instancio la clase
    def __init__(self, latitud, longitud, address, area, rooms, garage):
        self.latitud= latitud
        self.longitud=longitud
        self.address= address
        self.area= area
        self.rooms= rooms 
        self.garage= garage

#metodo para crear la tabla 
db.create_all()

#defino un schema 

class TaskSchema(ma.Schema):
    class Meta:
        #defino los campos que quiero obtener cada vez que interactue en este schema 
        fields=('id','latitud','longitud', 'address', 'area', 'rooms', 'garage')

#creo una variable que me permita eliminar o crear una tarea pueda interactuar 
task_schema= TaskSchema()
tasks_schema= TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():

    #recibimos la tarea
    latitud= request.json['latitud']
    longitud= request.json['longitud']
    address= request.json['address']
    area= request.json['area']
    rooms = request.json['rooms']
    garage= request.json['garage']

    #guardamos la tarea 
    new_task= Task( latitud, longitud, address , area , rooms , garage )
    db.session.add(new_task)
    db.session.commit()

    #desde schema convierto a json 
    #respuesta de la tarea para que el cliente vea lo que ha creado 
    return task_schema.jsonify(new_task)

    #para devolver todas las tareas

@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks= Task.query.all()
    result= tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
#para devolver tareas segun el id 
def get_task(id):
    task= Task.query.get(id)
    return task_schema.jsonify(task)

#para modificar
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    latitud= request.json['latitud']
    longitud= request.json['longitud']
    address= request.json['address']
    area= request.json['area']
    rooms = request.json['rooms']
    garage= request.json['garage']

    task.latitud = latitud
    task.longitud= longitud
    task.address = address 
    task.area = area
    task.rooms = rooms 
    task.garage = garage

    db.session.commit()
    return task_schema.jsonify(task)

#para eliminar tareas
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task= Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message':'Welcome to my API'})

if __name__=='__main__':
    app.run(debug=True)
    