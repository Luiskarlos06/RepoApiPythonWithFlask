from flask_restful import Api
from app.api import api_blue

api = Api(api_blue)

from .resources.login import Login
from .resources.users import Users
from .resources.tabledynamofunctions import GetAllUsers
from .resources.tabledynamofunctions import GetUsersByUserId
from .resources.tabledynamofunctions import AddUser
from .resources.tabledynamofunctions import DeleteUser
from .resources.tabledynamofunctions import UpdateUser



api.add_resource(Login,'/login',endpoint="login")
api.add_resource(Users,'/users/<string:user>',endpoint="users")
api.add_resource(GetAllUsers,'/tabledynamofunctions/GetAllUsers',endpoint="getallusers")
api.add_resource(GetUsersByUserId,'/tabledynamofunctions/GetUsersByUserId/<string:userid>',endpoint="getusersbyuserid")
api.add_resource(AddUser,'/tabledynamofunctions/AddUser',endpoint="adduser")
api.add_resource(DeleteUser,'/tabledynamofunctions/DeleteUser/<string:userid>',endpoint="deleteuser")
api.add_resource(UpdateUser,'/tabledynamofunctions/UpdateUser/<string:userid>',endpoint="updateuser")