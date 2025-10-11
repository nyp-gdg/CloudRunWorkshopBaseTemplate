from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .db import SessionLocal
from .models import User

bp = Blueprint("auth", __name__)

@bp.post("/register")
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"Error": "Username and Password is required."}), 400
    
    with SessionLocal() as db:
        if db.query(User).filter_by(username = username).first():
            return jsonify({"Error":"Username Taken"}), 409
        u = User(username = username, password_hash = generate_password_hash(password))
        db.add(u)
        db.commit()
    return jsonify({"Status": "Registered"}), 201

@bp.post("/login")
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    with SessionLocal() as db:
        u = db.query(User).filter_by(username = username).first()
        if not u or not check_password_hash(u.password_hash, password):
            return jsonify({"Error":"Invalid Credentials"}), 401
    session["user"] = username
    return jsonify({"Status" : "Ok", "User" : username})

@bp.get("/profile")
def profile():
    username = session.get("user")
    if not username:
        return jsonify({"Error" : "Unauthorized"}), 401
    return jsonify({"User" : username})
