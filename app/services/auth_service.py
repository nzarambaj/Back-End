from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import db
from app.models.user import User


def register_user(data):
    username = data.get("username")
    password = data.get("password")
    
    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 400
    
    user = User(
        username=username, 
        password=generate_password_hash(password),
        role=data.get("role", "user")
    )
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return {
        "message": "User registered successfully",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    }, 201


def login_user(data):
    username = data.get("username")
    password = data.get("password")
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))  # Convert ID to string
        
        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }, 200
    
    return {"error": "Invalid credentials"}, 401