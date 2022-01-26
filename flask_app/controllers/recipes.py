from flask import render_template, request, redirect, flash, session
from flask_app.models import recipe
from flask_app import app

@app.route('/recipes/add')
def add_recipe():
  if 'user_id' not in session:
    return redirect("/")
  title = "Create a new recipe"
  data = {
        "id": 0,
        "name": "",
        "description": "",
        "instructions": "",
        "created_at":"",
        "updated_at":"",
        "made_at": "",
        "is_under_30": ""
    }
  recipeObj = recipe.Recipe(data)
  return render_template("form_recipe.html",title=title,recipeObj=recipeObj)

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    title = "Edit recipe"
    recipeObj = recipe.Recipe.get_recipe_by_id({"id":id})
    return render_template("form_recipe.html", title=title,recipeObj=recipeObj)

@app.route("/recipes/delete/<int:id>")
def delete_recipe(id):
    recipe.Recipe.delete({"id":id})
    return redirect("/")

@app.route("/recipes/<int:id>")
def view_recipe(id):
    recipeObj = recipe.Recipe.get_recipe_by_id({"id":id})
    return render_template("view_recipe.html",recipeObj=recipeObj)

@app.route('/recipes/save', methods=["POST"])
def save_recipe():
    if(request.form["id"] != "0"):
      data2 = {
        "id": request.form["id"],
        "name": request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "made_at": request.form["made_at"],
        "is_under_30": request.form["is_under_30"],
      }
      recipe.Recipe.update(data2)
    else:
      recipe.Recipe.save(request.form)
    return redirect('/')