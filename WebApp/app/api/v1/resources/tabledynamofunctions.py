from flask import Flask, jsonify, request
import json
import boto3
from flask_restful import Resource
from app.auth import auth, conex_dynamo as c

def suma(x,y):
    return x + y


class GetAllUsers(Resource):
    print ("Resource",Resource)
    decorators=[auth.login_required]
 
    def get(self):
        print ("self",self)
        try:
            client = c.conex_dynamo()
            response = client.scan(TableName='users-table')
            items = response["Items"]

            return items,200

        except:
            print("An exception occurred")
            return dict(message = 'Se ha presentado un error en la ejecución de la petición'),400
 
class GetUsersByUserId(Resource):
    decorators=[auth.login_required] 
 
    def get(self, userid):
        client = c.conex_dynamo()

        try:
            response = client.get_item(TableName='users-table', Key={'userid':{'S':str(userid)}})
            if 'Item' in response:
                return response['Item'],200
        
            else:
                return dict(message = 'No se han encontrado registros asociados al userid ingresado.'),200

        except:
            print (response)
            return dict(message = 'Se ha presentado un error en la ejecución de la petición'),400



class AddUser(Resource):
    decorators=[auth.login_required]

    def post(self):
        userid = request.get_json().get('userid')
        username = request.get_json().get('username')
        age = request.get_json().get('age')

        if (userid == None or username == None or age == None):
            return dict(message = 'Verifique datos ingresados.'),200


        client = c.conex_dynamo()

        #Buscar usuario para asegurarse que no exista en la tabla antes de crearlo


        response = client.get_item(TableName='users-table', Key={'userid':{'S':str(userid)}})
        if 'Item' in response:
            return dict(message = 'Ya se encuentra un usuario creado en la tabla con el userid ingresado.'),200
        
        else: 
            try:
                response = client.put_item(TableName='users-table', 
                                        Item={'userid':{'S':str(userid)},     
                                                'username':{'S':str(username)},
                                                'age':{'S':str(age)}
                                        })
                return dict(message = 'Registro creado correctamente en la tabla.'),200
            except:
                print("An exception occurred")
                return dict(message = 'Se ha presentado un error en la ejecución de la petición, COD 004.'),400

# Borrar usuarios
class DeleteUser(Resource):
    decorators=[auth.login_required]

    def delete(self, userid):

        client = c.conex_dynamo()
        try:
            
            response = client.get_item(TableName='users-table', Key={'userid':{'S':str(userid)}})
            if 'Item' in response:
                response = client.delete_item(TableName='users-table', Key={'userid':{'S':str(userid)}})
                print (response)
                return dict(message = 'Registro eliminado correctamente en la bd.'),200

            else:
                return dict(message = 'No se encuentra el userid en la base de datos. No se eliminó ningún registro en bd.'),200
    
        except:
            return dict(message = 'Se ha presentado un error en la ejecución de la petición, COD 004.'),400

# Actualizar usuarios
class UpdateUser(Resource):
    decorators=[auth.login_required]

    def put(self, userid):
        try:
            username = request.get_json().get('username')
            age = request.get_json().get('age')
        except:
            return dict(message = 'Verifique datos ingresados.'),200


        if (userid == None or username == None or age == None):
            return dict(message = 'Verifique datos ingresados.'),200
        

        client = c.conex_dynamo()

        try:
            response = client.get_item(TableName='users-table', Key={'userid':{'S':str(userid)}})
            if 'Item' in response:
                response = client.put_item(TableName='users-table', 
                                            Item={'userid':{'S':str(userid)},     
                                                    'username':{'S':str(username)},
                                                    'age':{'S':str(age)}
                                            })
                
                return dict(message = 'Registro actualizado correctamente en la bd.'),200
            else:
                return dict(message = 'No se ha encontrado el userid en la bd. No se actualizó ningún registro en la base de datos.'),200
                
        except:
            print("An exception occurred")
            return "Se ha presentado un error en la ejecución de la petición, COD 004", 400

