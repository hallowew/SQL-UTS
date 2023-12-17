# Inisialisasi Library
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet


#Inisialisasi app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@127.0.0.1/db_uts'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

#Inisialisasi encrypt AES
key = Fernet.generate_key()
cipher_suite = Fernet(key)

#Definet Model User
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column (db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)


#API
#Get All Users
@app.route('/api/users', methods=['GET'])
def get():
    users = User.query.all();
    data = []
    for user in users:
        
        data.append({'username': user.username, 'password' : user.password})
    
    return jsonify({'users' : data})

# Create new user
@app.route('/api/users', methods=['POST'])
def create() :
    data = request.get_json()
    user = User(id=data['id'], username=data['username'], password=cipher_suite.encrypt(data['password'].encode()).decode())
    db.session.add(user)
    db.session.commit()

    return jsonify({'message' : 'User Successfully created'}), 201


#Get Detail user
@app.route('/api/users/<id>', methods=['GET'])
def show(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return jsonify({"id" : user.id, "username" : user.username, "password" : user.password }), 200
    
    return jsonify({"message" : "User not found"}), 404
    
#Update data user
@app.route('/api/users/<id>', methods=['PUT'])
def update(id):
    user = User.query.filter_by(id=id).first()
    if user:
        data = request.get_json()
        user.username = data['username']
        user.password = cipher_suite.encrypt(data['password'].encode()).decode()
        db.session.commit()
        return jsonify({"message" : "User Updated Successfully"})
    
    return jsonify({"message" : "User not found"}), 404

#Delete
@app.route('/api/users/<id>', methods=['DELETE'])
def destroy(id):
    user = User.query.filter_by(id=id).first()
    if user:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message":"User deleted successfully"})
    return jsonify({"message":"User Not Found"}), 404


if __name__ == '__main__':
    app.run(debug=True)