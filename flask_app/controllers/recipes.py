from flask import render_template, request, redirect, flash, session
from flask_app.models import recipe,alimento
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
  return render_template("form_recipe.html",title=title,recipeObj=recipeObj,alimentos=alimento.Alimento.get_all())

@app.route("/recipes/edit/<int:id>")
def edit_recipe(id):
    title = "Edit recipe"
    recipeObj = recipe.Recipe.get_recipe_by_id({"id":id})
    alimentos = alimento.Alimento.get_all()
    for alimentoAux in alimentos:
      for alimentoChecked in recipeObj.ingredientes:
        if alimentoAux.id == alimentoChecked.id:
          alimentoAux.checked = "1"
    return render_template("form_recipe.html", title=title,recipeObj=recipeObj,alimentos=alimentos)

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

      recipe_id = request.form["id"]
      recipeAux = recipe.Recipe.get_recipe_by_id({"id":recipe_id})
      list_update = request.form.getlist('foodOption')
      list_actual_arr = list(map(lambda x : str(x.id),recipeAux.ingredientes)) 
      list_actual = recipeAux.ingredientes
      if list_actual[0].id != None:
        for food_actual in list_actual:
          if str(food_actual.id) not in list_update:
            ingredient_id = alimento.Alimento.get_ingredient_id({"recipe_id":int(recipe_id),"alimento_id":int(food_actual.id)})
            alimento.Alimento.delete_ingredient({"id":int(ingredient_id["id1"])})
      
      for food_update in list_update:
        if food_update not in list_actual_arr:
          alimento.Alimento.save_ingredient({"recipe_id":int(recipe_id),"alimento_id":int(food_update)})

    else:
      checked = request.form.getlist('foodOption')
      id = recipe.Recipe.save(request.form)
      for checkFood in checked:
        alimento.Alimento.save_ingredient({"recipe_id":id,"alimento_id":checkFood})
    return redirect('/')