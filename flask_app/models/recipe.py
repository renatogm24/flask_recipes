from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import alimento

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
        self.ingredientes = []
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes (name, description, instructions , is_under_30, made_at, created_at, updated_at, user_id ) VALUES ( %(name)s , %(description)s ,%(instructions)s ,%(is_under_30)s ,%(made_at)s ,NOW() , NOW(), %(user_id)s );"
        return connectToMySQL('flask_recipes_w_checkbox').query_db( query, data )

    @classmethod
    def update(cls, data ):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions=%(instructions)s , is_under_30=%(is_under_30)s, made_at=%(made_at)s,  updated_at = NOW() where id = %(id)s;"
        return connectToMySQL('flask_recipes_w_checkbox').query_db( query, data )

    @classmethod
    def delete(cls, data ):
        query = "DELETE from recipes where id = %(id)s;"
        return connectToMySQL('flask_recipes_w_checkbox').query_db( query, data )

    @classmethod
    def get_recipe_by_id(cls,data):
        query = "SELECT * FROM recipes left join ingredientes on recipes.id = ingredientes.recipe_id left join alimentos on alimentos.id = ingredientes.alimento_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL('flask_recipes_w_checkbox').query_db(query,data)
        if len(results) < 1:
          return False
        recipe = cls(results[0])
        for alimentoAux in results:
          data = {
            "id": alimentoAux["alimentos.id"],
            "name" : alimentoAux["alimentos.name"],
            "created_at" : alimentoAux["alimentos.created_at"],
            "updated_at" : alimentoAux["alimentos.updated_at"]
          }
          recipe.ingredientes.append(alimento.Alimento(data))
        return recipe

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
