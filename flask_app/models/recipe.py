from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.is_under_30 = data['is_under_30']
        self.made_at = data['made_at']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes (name, description, instructions , is_under_30, made_at, created_at, updated_at, user_id ) VALUES ( %(name)s , %(description)s ,%(instructions)s ,%(is_under_30)s ,%(made_at)s ,NOW() , NOW(), %(user_id)s );"
        return connectToMySQL('flask_recipes').query_db( query, data )

    @classmethod
    def update(cls, data ):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions=%(instructions)s , is_under_30=%(is_under_30)s, made_at=%(made_at)s,  updated_at = NOW() where id = %(id)s;"
        return connectToMySQL('flask_recipes').query_db( query, data )

    @classmethod
    def delete(cls, data ):
        query = "DELETE from recipes where id = %(id)s;"
        return connectToMySQL('flask_recipes').query_db( query, data )

    @classmethod
    def get_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL('flask_recipes').query_db(query,data)
        if len(results) < 1:
          return False
        a = cls(results[0])
        print(a.name)
        return a

    @staticmethod
    def validate_recipe(recipe):
      is_valid = True 
      if len(recipe["name"])<3:
        flash("Name cant be empty or less than 3 letters","recipe")
        is_valid = False
      if len(recipe["description"])<3:
        flash("Description cant be empty or less than 3 letters","recipe")
        is_valid = False
      if len(recipe["instructions"])<3:
        flash("Instructions cant be empty or less than 3 letters","recipe")
        is_valid = False
      return is_valid
