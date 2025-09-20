from werkzeug.security import generate_password_hash
from config.extensions import db
from flask import request, jsonify
from models.user import User, user_schema, users_schema


class UserService:
    def get_users():
        name = request.args.get('name')
        if name:
            users = User.query.filter(User.name.ilike(f'%{name}%')).all()
        else:
            users = User.query.all()
        if users:
            result =  users_schema.dump(users)
            return jsonify({'message': 'sucessfully fetched', 'data': result.data})
        
        return jsonify({'message': 'no users found', 'data': {}})

    def post_user():
        name = request.json['username']
        password = request.json['password']
        email = request.json['email']
        role = request.json['role']

        user = user_by_email(email)
        if user:
            result = user_schema.dump(user)
            return jsonify({'message': 'user already exists', 'data': {}})

        pass_hash = generate_password_hash(password)
        user = User(name, pass_hash, role, email)

        try:
            db.session.add(user)
            db.session.commit()
            result = user_schema.dump(user)
            return jsonify({'message': 'successfully registered', 'data': result.data}), 201
        except:
            return jsonify({'message': 'unable to create', 'data': {}}), 500



    def user_by_email(self, email):
        return User.query.filter(User.email == email)
