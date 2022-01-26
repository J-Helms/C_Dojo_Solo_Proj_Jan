from solo_project_app.config.mysqlconnection import connectToMySQL
from solo_project_app import app
from solo_project_app.models.pet import Pet
from flask import flash
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

class User:
    db = "solo_project_db"
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.pets = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (username, first_name, last_name, password, created_at, updated_at) VALUES (%(username)s, %(first_name)s, %(last_name)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_user_by_username(cls, data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])


    @staticmethod
    def validate_user_register(user):
        is_valid = True
        if len(user['username']) < 2:
            flash("Username must be at least 2 characters in length.")
            is_valid = False
        if len(user['first_name']) < 1:
            flash("First name must be at least 1 character in length.")
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last name must be at least 1 character in length.")
            is_valid = False
        if len(user['password']) < 7:
            flash("Password must contain at least 7 characters")
            is_valid = False
        if not (user['confirm_password']) == (user['password']):
            flash("Passwords must match")
            is_valid = False
        return is_valid