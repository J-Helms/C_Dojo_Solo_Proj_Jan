from solo_project_app.config.mysqlconnection import connectToMySQL
from solo_project_app import app
from solo_project_app.models import user
from flask import flash, request, redirect, session
import re


class Pet:
    db = 'solo_project_db'
    def __init__(self, data):
        self.id = data['id']
        self.pet_name = data['pet_name']
        self.species = data['species']
        self.breed = data['breed']
        self.age = data['age']
        self.fixed = data['fixed']
        self.vet = data['vet']
        self.own_name = data['own_name']
        self.own_call = data['own_call']
        self.own_email = data['own_email']
        self.vacs_rabies_date = data['vacs_rabies_date']
        self.vacs_rabies_duration = data['vacs_rabies_duration']
        self.vacs_bord_date = data['vacs_bord_date']
        self.vacs_bord_duration = data['vacs_bord_duration']
        self.vacs_dis_date = data['vacs_dis_date']
        self.vacs_dis_duration = data['vacs_dis_duration']
        self.vacs_fvrc_date = data['vacs_fvrc_date']
        self.vacs_fvrc_duration = data['vacs_fvrc_duration']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def create_pet(cls, data):
        query = "INSERT INTO pets (pet_name, species, breed, age, fixed, vet, own_name, own_call, own_email, vacs_rabies_date, vacs_rabies_duration, vacs_bord_date, vacs_bord_duration, vacs_dis_date, vacs_dis_duration, vacs_fvrc_date, vacs_fvrc_duration, notes, created_at, updated_at, user_id) VALUES (%(pet_name)s, %(species)s, %(breed)s, %(age)s, %(fixed)s, %(vet)s, %(own_name)s, %(own_call)s, %(own_email)s, %(vacs_rabies_date)s, %(vacs_rabies_duration)s, %(vacs_bord_date)s, %(vacs_bord_duration)s, %(vacs_dis_date)s, %(vacs_dis_duration)s, %(vacs_fvrc_date)s, %(vacs_fvrc_duration)s, %(notes)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one_pet(cls, data):
        query = "SELECT * FROM pets WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        return(cls(results[0]))
        
    @classmethod
    def get_pet_with_user(cls, data):
        query = "SELECT * FROM pets LEFT JOIN users ON pets.user_id = users.id WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query)

    @classmethod
    def update_pet(cls, data):
        query = "UPDATE pets SET pet_name=%(pet_name)s, species=%(species)s, breed=%(breed)s, age=%(age)s, fixed=%(fixed)s, vet=%(vet)s, own_name=%(own_name)s, own_call=%(own_call)s, own_email=%(own_email)s, vacs_rabies_date=%(vacs_rabies_date)s, vacs_rabies_duration=%(vacs_rabies_duration)s, vacs_bord_date=%(vacs_bord_date)s, vacs_bord_duration=%(vacs_bord_duration)s, vacs_dis_date=%(vacs_dis_date)s, vacs_dis_duration=%(vacs_dis_duration)s, vacs_fvrc_date=%(vacs_fvrc_date)s, vacs_fvrc_duration=%(vacs_fvrc_duration)s, notes=%(notes)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_pets(cls):
        query = "SELECT * FROM pets;"
        results = connectToMySQL(cls.db).query_db(query)
        pets = []
        for pet in results:
            pets.append(cls(pet))
        return pets

    @classmethod
    def delete_pet(cls, data):
        query = "DELETE FROM pets WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @staticmethod
    def validate_pet(pet):
        is_valid = True
        if len(pet['pet_name']) < 1:
            flash('Pet name must be at least one(1) character.')
            is_valid = False
        if len(pet['own_name']) == False:
            flash("Owner's name must be included.")
            is_valid = False
        if len(pet['own_call']) < 1:
            flash("Owner's best contact number(#) must be included.")
            is_valid = False
        if len(pet['vet']) < 1:
            flash('A valid Veterinary Clinic or Veterinarian must be included.')
            is_valid = False
        return is_valid
