from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class Alimento:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.checked = "0"

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM alimentos;"
        results = connectToMySQL('flask_recipes_w_checkbox').query_db(query)
        if len(results) < 1:
          return False
        alimentos = []
        for alimento in results:
          alimentos.append(cls(alimento))
        return alimentos

    @classmethod
    def save_ingredient(cls,data):
        query = "INSERT INTO ingredientes (recipe_id, alimento_id) VALUES(%(recipe_id)s,%(alimento_id)s);"
        results = connectToMySQL('flask_recipes_w_checkbox').query_db(query,data)
        return results

    @classmethod
    def delete_ingredient(cls,data):
        query = "DELETE from ingredientes where id=%(id)s;"
        results = connectToMySQL('flask_recipes_w_checkbox').query_db(query,data)
        return results

    @classmethod
    def get_ingredient_id(cls,data):
        query = "SELECT ingredientes.id as id1 FROM ingredientes where ingredientes.recipe_id = %(recipe_id)s and ingredientes.alimento_id = %(alimento_id)s;"
        results = connectToMySQL('flask_recipes_w_checkbox').query_db(query,data)
        if len(results) < 1:
          return False
        return results[0]