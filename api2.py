from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    ccnumber = db.Column(db.String(80), unique=True, nullable=False)
    ccexpiration = db.Column(db.String(80), unique=True, nullable=False)
    ccsecuritycode = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"User(username = {self.username}, password = {self.password}, ccnumber = {self.ccnumber}, ccexpiration = {self.ccexpiration}, ccsecuritycode = {self.ccsecuritycode})"
    
user_args = reqparse.RequestParser() 
user_args.add_argument('username', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank")
user_args.add_argument('ccnumber', type=str, required=True, help="CCNumber cannot be blank")
user_args.add_argument('ccexpiration', type=str, required=True, help="CCExpiration cannot be blank")
user_args.add_argument('ccsecuritycode', type=str, required=True, help="CCSecurityCode cannot be blank")

userFields = {
    'id':fields.Integer,
    'username':fields.String,
    'password':fields.String,
    'ccnumber':fields.String,
    'ccexpiration':fields.String,
    'ccsecuritycode':fields.String,
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(username=args["username"], password=args["password"], ccnumber=args["ccnumber"], ccexpiration=args["ccexpiration"], ccsecuritycode=args["ccsecuritycode"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201
    
class User(Resource):
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        return user
    
    @marshal_with(userFields)
    def patch(self, id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        user.username = args["username"]
        user.password = args["password"]
        user.ccnumber = args["ccnumber"]
        user.ccexpiration = args["ccexpiration"]
        user.ccsecuritycode = args["ccsecuritycode"]
        db.session.commit()
        return user
    
    @marshal_with(userFields)
    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 200

api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True) 