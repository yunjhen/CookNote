import os
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404

from django.db.models import Q
from decimal import *
import uuid

from .models import Recipe, Recipe_Photo, Step, Step_Photo
from ingredients.models import Used_Ingredient, Ingredient, Nutrition_Facts
from ingredients.views import create_or_update_object, NutritionFactsInformation


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe_list.html'
    context_object_name = 'recipes'
    
class RecipeDetailView(DetailView):
    model = Recipe

    def get_context_data(self, **kwargs):
        detail_context = super().get_context_data(**kwargs)
        recipe = kwargs['object']
        nutrition_facts = recipe.get_nutrition_facts()
        if nutrition_facts:
            nutrition_facts = nutrition_facts[0]
        used_ingredients = recipe.get_used_ingredients()

        quantityUseds = []
        units = []
        calories = []
        for used_ingredient in used_ingredients:
            ingredient = used_ingredient.ingredient
            calories_ = ingredient.get_nutrition_facts()[0].calories
            serving = used_ingredient.serving

            quantityUseds.append(( ingredient.quantity * serving ).quantize(Decimal('1.00')))
            units.append(ingredient.unit)
            calories.append(( calories_ * serving ).quantize(Decimal('1.00')))
        # print("========= steps ==========")
        # print(recipe.get_steps())

        detail_context.update({
            'recipe': recipe,
            'used_ingredients': zip(used_ingredients, quantityUseds, units, calories),
            'steps': recipe.get_steps(),
            'nutrition_facts': nutrition_facts,
            })
        return detail_context

## 取得 input 的值 
class GetInputValue():
    def __init__(self, request):
        self.request = request

    def check_input(self, input, default='0'):
        if input:
            return input
        else:
            return default

    def get_step(self):
        if 'step_photo' in self.request.FILES:
            step_photo = self.request.FILES['step_photo']
        else:
            step_photo = ''

        return {
            'step': int(self.request.POST.get('step')),
            'step_photo': step_photo,
            'description': self.request.POST.get('description', ''),
            'notes': self.request.POST.get('notes', ''),
        }

    def get_recipe(self):
        if 'delicacy_photo' in self.request.FILES:
            delicacy_photo = self.request.FILES['delicacy_photo']
        else:
            delicacy_photo = ''
        
        return {
            'delicacy': self.request.POST.get('delicacy'),
            'introduction': self.request.POST.get('introduction'),
            'delicacy_photo': delicacy_photo,
            'delicacy_type': self.request.POST.get('delicacy_type'),
            'category': self.request.POST.get('category'),
            'cooking_time': int(self.check_input(self.request.POST.get('cooking_time'))),
            'servings': int(self.request.POST.get('servings')),
            'reference': self.check_input(self.request.POST.get('reference'), ''),
            'memo_text': self.check_input(self.request.POST.get('memo_text'), ''),
            'storage_method': self.check_input(self.request.POST.get('storage_method'), ''),
        }

## 取得 Form 中 input 的值 
class GetFormValue():
    def __init__(self, form):
        self.form = form

    def get_recipe(self):
        return {
            'delicacy': self.form.cleaned_data['delicacy'],
            'introduction': self.form.cleaned_data['introduction'],
            'delicacy_photo': self.form.cleaned_data['delicacy_photo'],
            'delicacy_type': self.form.cleaned_data['delicacy_type'],
            'category': self.form.cleaned_data['category'],
            'cooking_time': self.form.cleaned_data['cooking_time'],
            'servings': self.form.cleaned_data['servings'],
            'reference': self.form.cleaned_data['reference'],
            'memo_text': self.form.cleaned_data['memo_text'],
            'storage_method': self.form.cleaned_data['storage_method'],
        }

## 計算料理的營養成分
class CalculationNutritionFacts():
    def __init__(self, request=None):
        self.request = request

    # 回傳所有營養成分數值為0的字典
    def initial_nutrition_facts(self):
        return {
            'calories': Decimal('0'),
            'protein': Decimal('0'),
            'total_fat': Decimal('0'),
            'saturated_fat': Decimal('0'),
            'trans_fat': Decimal('0'),
            'polyunsaturated_fat': Decimal('0'),
            'monounsaturated_fat': Decimal('0'),
            'carbohydrate': Decimal('0'),
            'sugar': Decimal('0'),
            'sodium': Decimal('0'),
        
            'potassium': Decimal('0'),
            'calcium': Decimal('0'),
            'iron': Decimal('0'),
            'zinc': Decimal('0'),
        
            'dietary_fiber': Decimal('0'),
            'cholesterol': Decimal('0'),
        
            'vitamin_a': Decimal('0'),
            'vitamin_d': Decimal('0'),
            'vitamin_e': Decimal('0'),
            'vitamin_k': Decimal('0'),
            'vitamin_b1': Decimal('0'),
            'vitamin_b2': Decimal('0'),
            'niacin': Decimal('0'),
            'vitamin_b6': Decimal('0'),
            'vitamin_b12': Decimal('0'),
            'folate': Decimal('0'),
            'vitamin_c': Decimal('0'),
        }

    def sum_dictionary_value(self, dict1: dict, dict2: dict):
        for key in dict1.keys():
            dict1[key] = dict1[key]+dict2[key]
            
        return dict1
    
    def average_dictionary_value(self, dict: dict, divisor):
        for key, value in dict.items():
            dict[key] = (value/divisor).quantize(Decimal('1.00'))

        return dict

    # 計算料理的總熱量
    def calculate_nutrition_facts(self, used_ingredients_session, servings):
        nutrition_facts = self.initial_nutrition_facts()

        for used_ingredient in used_ingredients_session:
            current_nutrition_facts = used_ingredient.get('used_ingredient').get_nutrition_facts_dict()
            nutrition_facts = self.sum_dictionary_value(nutrition_facts, current_nutrition_facts)
            
        nutrition_facts = self.average_dictionary_value(nutrition_facts, servings),
        nutrition_facts_context = nutrition_facts[0]

        return nutrition_facts_context   

## 取得並儲存料理的營養成分 (每次新增食材、修改食材或是修改食譜"且該食譜已有加入的食材"時，都會執行一次該函式)
def get_and_save_recipe_calculate_nutrition(request):
    if 'recipe' in request.session and 'used_ingredients' in request.session:
        try:
            used_ingredients_session = request.session['used_ingredients']
            recipe = request.session['recipe']
            servings = recipe.servings

            calculateNutritionFacts = CalculationNutritionFacts()
            nutritionFacts = calculateNutritionFacts.calculate_nutrition_facts(used_ingredients_session, servings)

            request.session['nutrition_facts'] = nutritionFacts
            return True
        except Exception as e:
            print("======== ERROR <Function:get_and_save_recipe_calculate_nutrition> ========\n", e)
            print()
            return False
    else:
        return False

## 從 session 中取得食譜的資訊 (包含'recipe', 'nutrition_facts', 'used_ingredients' 及 'steps')
def get_recipe_context(request):
    context = {}

    if 'recipe' in request.session:
        recipe = request.session.get('recipe', {}) 
        context.update({'recipe': recipe})

    if 'nutrition_facts' in request.session:
        nutrition_facts = request.session.get('nutrition_facts', {})
        context.update({'nutrition_facts': nutrition_facts})

    if 'used_ingredients' in request.session:
        context['session'] = True
        used_ingredients = request.session.get('used_ingredients', {})
        context.update({'used_ingredients': used_ingredients})

    if 'steps' in request.session:
        context['session'] = True
        steps = request.session.get('steps', {})
        context.update({'steps': steps})

    if 'add-recipe' in request.session:
        context.update({'add_recipe': True})

    is_valid = False
    if 'used_ingredients' in request.session and 'steps' in request.session:
        if len(request.session['used_ingredients'])>0 and len(request.session['steps'])>0:
            is_valid = True
        
    context.update({'valid': is_valid})

    return context

##### 以下為加入食材會用到的函式 #####
## 以食材名稱來搜尋要加入的食材
def search_ingredient_view(request):
    return render(request, 'ingredients/ingredient_search.html', {'recipe': True})


## 設定要存入 session['used_ingredients'] 中的食材資訊
def set_used_ingredients_session_context(used_ingredient: Used_Ingredient):
    return {
        'used_ingredient': used_ingredient,
        'quantity_used': used_ingredient.get_quantity_used(),
        'calories': used_ingredient.get_calories(),
        'nutrition_facts': used_ingredient.get_nutrition_facts_dict,
    }

## 修改關於與食材有關的 session ，透過 session_key 決定要修改的 session 為何，完成動作後回傳該食材(object)
#  session_key 包含： 'add_used_ingredients', 'save_used_ingredients'
def update_used_ingredients_session(request, session_key:str, used_ingredient):
    try:
        if session_key in request.session:
            used_ingredients_session = request.session.get(session_key)
            if used_ingredient in used_ingredients_session:
                print("====== UPDATE <"+ session_key +"> ======\n", used_ingredient, "\n")
                used_ingredient.serving = Decimal(request.POST.get('serving'))
                return used_ingredient

        used_ingredient.serving = Decimal(request.POST.get('serving'))
        add_to_session(request, session_key, used_ingredient)
        return used_ingredient

    except Exception as e:
        print('======== ERROR <remove_and_appeand_to_used_ingredients_session> ========\n', e)


## 新增食材 (存入 session['used_ingredients'] 中, 這裡用到的pk會在儲存到資料庫前刪除)
def add_used_ingredient_view(request, ingredient_id):
    if request.method == 'POST':
        if request.POST.get('serving'):
            used_ingredient = Used_Ingredient()
            used_ingredient.pk = uuid.uuid4()
            used_ingredient.recipe = request.session['recipe']
            used_ingredient.ingredient = get_object_or_404(Ingredient, pk=request.POST.get('ingredient_id'))
            used_ingredient.serving = Decimal(request.POST.get('serving'))

            print("======== add_used_ingredient ========\n", used_ingredient, "\n")
            add_to_session(request, 'add_used_ingredients', used_ingredient)
            
            used_ingredient_ = set_used_ingredients_session_context(used_ingredient)
            add_to_session(request, 'used_ingredients', used_ingredient_)
            
        get_and_save_recipe_calculate_nutrition(request)

        return HttpResponseRedirect(reverse('edit-recipe-step2'))

    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    nutrition_facts = ingredient.get_nutrition_facts()[0]
    if ingredient != None:
        context = {
            'ingredient': ingredient,
            'nutrition_facts': nutrition_facts,
        }
        return render(request, 'recipes/used_ingredient_add.html', context)

## 修改食材 (修改 session['used_ingredients']，將原先的食材刪除，並將修改後的食材加到 session['used_ingredients'] 中)
#  如果修改的食材為本次編輯時所新增的，會更新 session['add_used_ingredients'] 中的內容
#  如果修改的食材 非 本次編輯時所新增的，則會更新 session['save_used_ingredients'] 中的內容
def edit_used_ingredient_view(request):
    if request.method == 'POST':
        if request.POST.get('serving'):
            pk = request.POST.get('pk')
            used_ingredients_session = request.session.get('used_ingredients')

            for used_ingredient_ in used_ingredients_session:
                used_ingredient = used_ingredient_['used_ingredient']

                if str(used_ingredient.pk) == pk:
                    used_ingredients_session.remove(used_ingredient_)
                    if '-' in pk:
                        update_used_ingredient = update_used_ingredients_session(request, 'add_used_ingredients', used_ingredient)
                    else:
                        update_used_ingredient = update_used_ingredients_session(request, 'save_used_ingredients', used_ingredient)
                    
                    update_used_ingredient_ = set_used_ingredients_session_context(update_used_ingredient)
                    add_to_session(request, 'used_ingredients', update_used_ingredient_)
                    break
            
            get_and_save_recipe_calculate_nutrition(request)

            return HttpResponseRedirect(reverse('edit-recipe-step2'))
            
## 刪除食材 (將該食材從 session['used_ingredients'] 中刪除，並存到 session['delete_objects'] 當使用者按下儲存後，才會真正刪除該步驟)
def delete_used_ingredient_view(request, pk):
    if request.method == 'POST':
        try:
            used_ingredients_session = request.session.get('used_ingredients')

            for used_ingredient_ in used_ingredients_session:
                used_ingredient = used_ingredient_['used_ingredient']

                if str(used_ingredient.pk) == pk:
                    used_ingredients_session.remove(used_ingredient_)
                    if '-' in pk:
                        add_used_ingredients_session = request.session.get('add_used_ingredients', [])
                        if add_used_ingredients_session:
                            if used_ingredient in add_used_ingredients_session:
                                add_used_ingredients_session.remove(used_ingredient)
                                print("====== DELETE <used_ingredient not in DB> ======\n", used_ingredient, "\n")
                        break

                    else:
                        delete_used_ingredient = get_object_or_404(Used_Ingredient, pk=pk)

                        save_used_ingredients_session = request.session.get('save_used_ingredients', [])
                        if delete_used_ingredient in save_used_ingredients_session:
                            save_used_ingredients_session.remove(delete_used_ingredient)
                        add_to_session(request, 'delete_objects', delete_used_ingredient)
                        print("====== DELETE <used_ingredient in DB> ======\n", delete_used_ingredient, "\n")
                        break
        except Exception as e:
            print("========= ERROR <Function:delete_used_ingredient> =========\n", e)

        get_and_save_recipe_calculate_nutrition(request)

    return HttpResponseRedirect(reverse('edit-recipe-step2'))
    

## 將 used_ingredients 或 steps 存入 session[session_key] 中
#  session_key 包含以下 7 個:
#    'used_ingredients', 'steps': 用於儲存要顯示在頁面上的資訊 <used_ingredients: dict, steps: objects>
#    'add_used_ingredients','add_steps': 用於記錄新增了哪些食材或步驟 <objects>
#    'save_used_ingredients','save_steps': 用於記錄要儲存(save())哪些食材或步驟 <objects>
#    'delete_objects': 用於記錄要刪除(delete())哪些食材、步驟或圖片(Recipe_Photo, Step_Photo) <objects>
def add_to_session(request, session_key:str, add_value):
    try:
        if session_key in request.session:
            session = request.session.get(session_key)
            session.append(add_value)
            request.session[session_key] = session
        else:
            request.session[session_key] = [add_value]
        
        print("========= SUCCESS <", session_key, "> =========\n", request.session[session_key], "\n")
    except Exception as e:
        print("========= ERROR <Function: add_to_session> =========\n", e)

## 依據步驟的編號(step)進行排序(asc)
def sort_step(steps):
    if len(steps) < 2:
        return steps
    else:
        pivot = steps[0]
        less = []
        greater = []
        for i in steps[1:]: 
            if int(i.step) <= int(pivot.step):
                less.append(i)
            else:
                greater.append(i)
        
        return sort_step(less) + [pivot] + sort_step(greater)

## 將圖片儲存到資料庫中，如果該物件已有圖片且該圖片不是於本次編輯時所新增的，會將原本的圖片加進 session['delete_objects'] 中
def save_photo(request, model, photo, obj=None):
    if obj:
        photos = request.session.get('add_photos', [])
        if obj.photo not in photos  and  obj.photo:
            add_to_session(request, 'delete_objects', obj.photo)
           
    model.photo = photo
    model.save()
    add_to_session(request, 'add_photos', model)
    
    return model

## 將取得關於步驟的 input 並回傳該步驟(object)
def get_step_input(request, step):
    step.step = request.POST.get('step')
    step.description = request.POST.get('description')
    step.notes = request.POST.get('notes')

    if 'step_photo' in request.FILES:
        photo = save_photo(request, Step_Photo(), request.FILES.get('step_photo'), obj=step)
        step.photo = photo

    return step

## 修改關於與步驟有關的 session ，透過 session_key 決定要修改的 session 為何，完成動作後回傳該步驟(object)
#  session_key 包含： 'add_steps', 'save_steps'
def update_steps_session(request, session_key:str, step):
    try:
        steps_session = request.session.get(session_key, {})
        if step in steps_session:
            step = get_step_input(request, step)
            print("====== UPDATE <"+ session_key +"> ======\n", request.session.get(session_key), "\n")
            return step

        step = get_step_input(request, step)
        add_to_session(request, session_key, step)
        return step
    except Exception as e:
        print("======== ERROR <Function: update_steps_session - key: "+session_key+"> ========\n", e)

    return step


## 新增步驟 (存入 session['steps'] 中)
def add_step_view(request):
    if request.method == 'POST':
        if request.POST.get('step') \
            and request.POST.get('description'):
        
            step = Step()
            step.pk = uuid.uuid4()
            step.recipe = request.session.get('recipe')
            step.step = request.POST.get('step')
            step.description = request.POST.get('description')
            step.notes = request.POST.get('notes')

            if 'step_photo' in request.FILES:
                photo = save_photo(request, Step_Photo(), request.FILES.get('step_photo'))
                step.photo = photo
                
            add_to_session(request, 'add_steps', step)
            add_to_session(request, 'steps', step)
            
            request.session['steps'] = sort_step(request.session.get('steps', [])) 

            return HttpResponseRedirect(reverse('edit-recipe-step2'))
    
## 修改步驟 (修改 session['steps']，將原先的步驟刪除，並將修改後的步驟加到 session['steps'] 中)
#  如果修改的步驟為本次編輯時所新增的，會更新 session['add_steps'] 中的內容
#  如果修改的步驟 非 本次編輯時所新增的，則會更新 session['save_steps'] 中的內容
def edit_step_view(request):
    if request.method == 'POST':
        if request.POST.get('step') \
            and request.POST.get('description'):
            try:
                step_pk = request.POST.get('pk')
                steps_session = request.session.get('steps')
                
                for step in steps_session:
                    if str(step.pk) == step_pk:
                        steps_session.remove(step) 
                        print("======= steps_session =======\n", steps_session)
                        if '-' in step_pk:
                            update_step = update_steps_session(request, 'add_steps', step)
                        else:
                            update_step = update_steps_session(request, 'save_steps', step)
                        
                        add_to_session(request, 'steps', update_step)

            except Exception as e:
                print('======== ERROR <Function: edit_step_view> ========\n', e)
            
            request.session['steps'] = sort_step(request.session.get('steps', []))  

            return HttpResponseRedirect(reverse('edit-recipe-step2'))

## 刪除步驟 (將該食材從 session['steps'] 中刪除，並存到 session['delete_objects'] 當使用者按下儲存後，才會真正刪除該步驟)
def delete_step_view(request, pk):
    if request.method == "POST":
        steps_session = request.session.get('steps')

        for step in steps_session:
            if str(step.pk) == pk:
                steps_session.remove(step) 
                if '-' in pk:
                    add_steps_session = request.session.get('add_steps', [])
                    if add_steps_session:
                        if step and (step in add_steps_session):
                            add_steps_session.remove(step)
                            print("====== DELETE <steps not in DB> ======\n", step, "\n")
                    break
                else:
                    delete_step = get_object_or_404(Step, pk=pk)
                    print("====== DELETE <steps in DB> ======\n", delete_step, "\n")

                    save_steps_session = request.session.get('save_steps', [])
                    if delete_step and (delete_step in save_steps_session):
                        save_steps_session.remove(delete_step)
                                
                    add_to_session(request, 'delete_objects', delete_step)
                    break

    request.session['steps'] = sort_step(request.session.get('steps', []))  
    return HttpResponseRedirect(reverse('edit-recipe-step2'))


## 將與食譜有關的資訊存入 session 中
def add_recipe_to_session(request, recipe:Recipe):
    ## 將食譜的資訊存入 session中 <object>
    request.session['recipe'] = recipe

    ## 將食譜的營養標示存入 session中 <dict>
    nutrition_facts = recipe.get_nutrition_facts()
    if nutrition_facts:
        nutrition_facts = NutritionFactsInformation(nutrition_facts[0]).get_nutrition_facts()
        request.session['nutrition_facts'] = nutrition_facts

    ## 將食譜中的步驟存入 session中
    steps = recipe.get_steps()
    try:
        if steps:
            steps_list = []
            for step in steps:
                steps_list.append(step)
            request.session['steps'] = steps_list
    
    except Exception as e:
        print("======== ERROR <Function: add_recipe_to_session> steps part ========\n", e)
        print()
    
    ## 將食譜中的食材存入 session中
    used_ingredients = recipe.get_used_ingredients()
    try:
        if used_ingredients:
            used_ingredients_list = []
            for used_ingredient in used_ingredients:
                used_ingredien_ = set_used_ingredients_session_context(used_ingredient)
                used_ingredients_list.append(used_ingredien_)
            request.session['used_ingredients'] = used_ingredients_list

    except Exception as e:
        print("======== ERROR <Function: add_recipe_to_session> used_ingredients part ========\n", e)
        print()

## 將與食譜有關的資訊從 session 中移除
def clear_recipe_session(request):
    try:
        if 'recipe' in request.session:
            del request.session['recipe']
        if 'used_ingredients' in request.session:
            del request.session['used_ingredients']
        if 'steps' in request.session:
            del request.session['steps']
        if 'nutrition_facts' in request.session:
            del request.session['nutrition_facts']

        if 'add-recipe' in request.session:
            del request.session['add-recipe']
        if 'edit-recipe' in request.session:
            del request.session['edit-recipe']
      
        if 'delete_objects' in request.session:
            del request.session['delete_objects']
        
        if 'save_used_ingredients' in request.session:
            del request.session['save_used_ingredients']
        if 'save_steps' in request.session:
            del request.session['save_steps']

        if 'add_used_ingredients' in request.session:
            del request.session['add_used_ingredients']

        if 'add_steps' in request.session:
            try:
                steps = request.session.get('add_steps', [])
                photos = request.session.get('add_photos', [])
                for step in steps:
                    if step.photo and (step.photo in photos):
                        photos.remove(step.photo)
                        step.photo.delete()
                for photo in photos:
                    photo.delete()
                    print("======= DELETE photo =======\n", photo)
            except Exception as e:
                print('======== ERROR <Function: clear_recipe_session> delete add_steps part ========\n', e)

            del request.session['add_steps']
            
        if 'add_photos' in request.session:
            try:
                photos = request.session.get('add_photos')
                print("======= add_photos =======\n", photos)
                for photo in photos:
                    photo.delete()
            except Exception as e:
                print('======== ERROR <Function: clear_recipe_session>  delete add_photos part ========\n', e)

            del request.session['add_photos']
        print('======== clear session ========')
    except KeyError as k:
        print('======== KEY ERROR <clear_recipe_session>', k, '========')
    
    return HttpResponseRedirect(reverse('recipe'))


## 新增食譜-步驟1 (輸入關於食譜的資訊，如果食譜已加入食材，在送出表單後會重新計算料理的營養成分)
def add_recipe_view(request):
    if request.method == 'POST':
        getInput = GetInputValue(request)
        recipe_ = getInput.get_recipe()

        if 'delicacy_photo' in recipe_:
            del recipe_['delicacy_photo']

        if 'recipe' in request.session:
            recipe = request.session['recipe']
            recipe_obj = create_or_update_object(recipe_, Recipe, recipe)
        else: 
            recipe_obj = create_or_update_object(recipe_, Recipe)

        if 'delicacy_photo' in request.FILES:
            photo = save_photo(request, Recipe_Photo(), request.FILES.get('delicacy_photo'), obj=recipe_obj)
            recipe_obj.photo = photo
            recipe_obj.save()

        request.session['recipe'] = recipe_obj
        get_and_save_recipe_calculate_nutrition(request)
        return HttpResponseRedirect(reverse('edit-recipe-step2'))

    if 'add-recipe' in request.session:
        context = {
            'recipe': request.session.get('recipe', {})
        }
        return render(request, 'recipes/recipe_add.html', context)
    else:
        clear_recipe_session(request)
        request.session['add-recipe'] = True

        return render(request, 'recipes/recipe_add.html')

## 修改食譜-步驟1 (修改關於食譜的資訊)
def edit_recipe_view(request, pk):
    if request.method == 'POST':        
        try:
            recipe = get_object_or_404(Recipe, pk=request.POST.get('pk'))
            
            getInput = GetInputValue(request)
            recipe_ = getInput.get_recipe()
            if 'delicacy_photo' in recipe_:
                del recipe_['delicacy_photo']

            if 'recipe' in request.session:
                recipe = request.session['recipe']
                recipe_obj = create_or_update_object(recipe_, Recipe, recipe)

                if 'delicacy_photo' in request.FILES:
                    photo = save_photo(request, Recipe_Photo(), request.FILES.get('delicacy_photo'), obj=recipe_obj)
                    recipe_obj.photo = photo
                    
                request.session['recipe'] = recipe_obj
            
            get_and_save_recipe_calculate_nutrition(request)
            return HttpResponseRedirect(reverse('edit-recipe-step2'))
        except Exception as e:
            print("======== ERROR <Function: edit_recipe> ========\n", e)
            print()

    if 'edit-recipe' in request.session:
        if request.session['edit-recipe'] == pk: 
            context = {
                'recipe': request.session.get('recipe', {}),
            }
            return render(request, 'recipes/recipe_edit.html', context)
    clear_recipe_session(request)

    recipe_obj = get_object_or_404(Recipe, pk=pk)
    add_recipe_to_session(request, recipe_obj)
    request.session['edit-recipe'] = pk
    context = get_recipe_context(request)

    return render(request, 'recipes/recipe_edit.html', context)


## 新增(修改)食譜-步驟2 (修改關於食譜的資訊)
def recipe_edit_step2_view(request):
    if request.method == "POST":
        try:
            nutrition_facts_ = request.session.get('nutrition_facts', {})

            recipe_obj = request.session.get('recipe', {})
            if 'edit-recipe' in request.session:
                recipe_obj.save()

            if recipe_obj.photo:
                add_photos_session = request.session.get('add_photos', [])
                print("====== recipe_obj.photo =======\n", recipe_obj.photo, "\n")
                if recipe_obj.photo and (recipe_obj.photo in add_photos_session):
                    add_photos_session.remove(recipe_obj.photo)

            nutrition_facts = recipe_obj.get_nutrition_facts()

            ## 更新營養標示
            if nutrition_facts:
                nutrition_facts = nutrition_facts[0]
                obj = create_or_update_object(nutrition_facts_, Nutrition_Facts, nutrition_facts)
                print("========= UPDATE nutrition_facts =========\n", obj, "\n")
            else:
                nutrition_facts_.update({'recipe': recipe_obj})
                obj = create_or_update_object(nutrition_facts_, Nutrition_Facts)
                print("========= CREATE nutrition_facts =========\n", obj, "\n")

            ## 從 session 中取出要刪除的食材與步驟，並從資料庫中刪除
            if 'delete_objects' in request.session:
                del_objects = request.session.get('delete_objects', [])
                for obj in del_objects:
                    try:
                        obj.delete()
                        print("========= DELETE <delete_objects> =========\n", obj)
                    except Exception as e:
                        print("========= ERROR <Function: recipe_edit_step2_view>  <delete_objects:", obj, "> =========\n", e)
                
                del request.session['delete_objects']

            ## 從 session 中取出要更新的食材，並更新資料庫中內容
            if 'save_used_ingredients' in request.session:
                save_used_ingredients = request.session.get('save_used_ingredients', [])
                
                for used_ingredients in save_used_ingredients:
                    try:
                        used_ingredients.save()
                        print("========= SAVE <save_used_ingredients> =========\n", used_ingredients)

                    except Exception as e:
                        print("========= ERROR <Function: recipe_edit_step2_view>  <save_used_ingredients:", used_ingredients, "> =========\n", e)
                
                del request.session['save_used_ingredients']


            ## 從 session 中取出要更新的步驟，並更新資料庫中內容
            if 'save_steps' in request.session:
                save_steps = request.session.get('save_steps', [])
                add_photos_session = request.session.get('add_photos', [])
                
                for step in save_steps:
                    try:
                        step.save()
                        if step.photo in add_photos_session:
                            add_photos_session.remove(step.photo)
                        print("========= SAVE <save_steps> =========\n", step)

                    except Exception as e:
                        print("========= ERROR <Function: recipe_edit_step2_view>  <save_steps:", step, "> =========\n", e)

                del request.session['save_steps']

            ## 從 session 中取出要新增的食材，並加入到資料庫中
            if 'add_used_ingredients' in request.session:
                used_ingredients_objects = request.session.get('add_used_ingredients', [])
                for used_ingredient in used_ingredients_objects:
                    try:
                        print("========= add_used_ingredients =========\n", used_ingredients_objects)
                        used_ingredient.pk = None
                        used_ingredient.save()
                        print("========= SAVE <add_used_ingredients> =========\n", used_ingredient)
                    except Exception as e:
                        print("========= ERROR <Function: recipe_edit_step2_view>  <add_used_ingredients:", used_ingredient, "> =========\n", e)
                
                del request.session['add_used_ingredients']

            ## 從 session 中取出要新增的步驟，並加入到資料庫中
            if 'add_steps' in request.session:
                steps_objects = request.session.get('add_steps', [])
                add_photos_session = request.session.get('add_photos', [])
                
                for step in steps_objects:
                    try:
                        step.pk = None
                        step.save()
                        if step.photo and (step.photo in add_photos_session):
                            add_photos_session.remove(step.photo)
                        print("========= SAVE <add_steps> =========\n", step)
                    except Exception as e:
                        print("========= ERROR <Function: recipe_edit_step2_view>  <add_steps:", step, "> =========\n", e)

                del request.session['add_steps']

            clear_recipe_session(request)
            return HttpResponseRedirect(reverse('recipe'))

        except Exception as e:
            print("======== ERROR <Function: recipe_edit_step2_view> ========\n", e)

    context = get_recipe_context(request)
    return render(request, 'recipes/recipe_edit_step2.html', context)


## 刪除食譜
def delete_recipe_view(request, recipe_id):
    if request.method == 'POST':
        try:
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            recipe.delete()

        except Exception as e:
            print("======== ERROR <Function: delete_recipe_view> ========", e)

    return HttpResponseRedirect(reverse('recipe'))


## 搜尋食材
def search_view(request):
    if request.method == "POST":
        try:
            search_text = request.POST['search_name']
            query_set1 = Recipe.objects.filter(Q(delicacy__contains=search_text)).order_by('-upload_date')
            query_set2 = Used_Ingredient.objects.filter(Q(ingredient__ingredient__contains=search_text) | Q(recipe__introduction__contains=search_text)).order_by('-recipe__upload_date')
            print(query_set1)
            print(query_set2)

            recipes = list(query_set1)
            print(recipes)

            for query in query_set2:
                if query.recipe not in recipes:
                    recipes.append(query.recipe)
            # recipes = Recipe.objects.filter(Q(delicacy__contains=search_text) | Q(introduction__contains=search_text))

            context={
                'search_text': search_text,
                'recipes': recipes,
            }   
            return render(request, 'recipes/recipe_list.html', context)
            
        except Exception as e:
            print("========== ERROR <Function: search_view> ==========\n", e)
            return HttpResponseForbidden()


