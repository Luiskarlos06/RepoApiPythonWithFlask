from flask_restful import Resource,request
from app.bd.users import users
from app import token_serializer

class Login (Resource):

    def post(self):

        try:
            _user = request.get_json().get('user')
            _passw = request.get_json().get('password')

        
            if (_user == None or _passw== None):
                return dict(message = 'Datos ingresados incorrectos, Verifica que el usuario y el password se encuentren diligenciados correctamente.'),400

            for user in users:
                if _user == user.get('user') and _passw == user.get('passw'):
                    token = token_serializer.dumps(dict(user = _user)).decode('utf-8')
                    return dict(message='Estas registado!', token = token), 201
            return dict(message = 'Usuario o contraseña no coinciden con los registros del sistema.'),400 
        except:
            return dict(message = 'Datos ingresados incorrectos, Verifica que el usuario y el password se encuentren diligenciados correctamente.'),400

