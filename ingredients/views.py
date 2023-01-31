from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Ingredient, Nutrition_Facts, Ingredient_File
from .forms import IngredientForm, NutritionFactsForm
from decimal import *
import pandas as pd
from http import HTTPStatus

class NutritionFactsInformation():
    def __init__(self, object=None):
        self.object = object
   
    def decimal_quantize(self, num):
        return Decimal(str(num))

    def get_label_list(self):
        return [
            'calories',
            'protein',
            'total_fat',
            'saturated_fat',
            'trans_fat',
            'carbohydrate',
            'sugar',
            'sodium',

            'polyunsaturated_fat', 
            'monounsaturated_fat',

            'potassium',
            'calcium',
            'iron',
            'zinc',

            'dietary_fiber',
            'cholesterol',
            
            'vitamin_a',
            'vitamin_d',
            'vitamin_e',
            'vitamin_k',
            'vitamin_b1',
            'vitamin_b2',
            'niacin',
            'vitamin_b6',
            'vitamin_b12',
            'folate',
            'vitamin_c',
        ]

    def get_nutrition_facts(self, factor=1):
        factor = self.decimal_quantize(factor)

        if self.object:
            return {
                'calories': self.object.calories*factor,
                'protein': self.object.protein*factor,
                'total_fat': self.object.total_fat*factor,
                'saturated_fat': self.object.saturated_fat*factor,
                'trans_fat': self.object.trans_fat*factor,
                'polyunsaturated_fat': self.object.polyunsaturated_fat*factor,
                'monounsaturated_fat': self.object.monounsaturated_fat*factor,
                'carbohydrate': self.object.carbohydrate*factor,
                'sugar': self.object.sugar*factor,
                'sodium': self.object.sodium*factor,

                'potassium': self.object.potassium*factor,
                'calcium': self.object.calcium*factor,
                'iron': self.object.iron*factor,
                'zinc': self.object.zinc*factor,
         
                'dietary_fiber': self.object.dietary_fiber*factor,
                'cholesterol': self.object.cholesterol*factor,
          
                'vitamin_a': self.object.vitamin_a*factor,
                'vitamin_d': self.object.vitamin_d*factor,
                'vitamin_e': self.object.vitamin_e*factor,
                'vitamin_k': self.object.vitamin_k*factor,
                'vitamin_b1': self.object.vitamin_b1*factor,
                'vitamin_b2': self.object.vitamin_b2*factor,
                'niacin': self.object.niacin*factor,
                'vitamin_b6': self.object.vitamin_b6*factor,
                'vitamin_b12': self.object.vitamin_b12*factor,
                'folate': self.object.folate*factor,
                'vitamin_c': self.object.vitamin_c*factor,
            }
        else:
            return {}

class GetInputValue():
    def __init__(self, request):
        self.request = request

    def check_input(self, dictionary:dict, names):
        for name in names:
            if self.request.POST.get(name):
                dictionary.update({
                    name: Decimal(self.request.POST.get(name))
                })
        return dictionary

    def get_nutrition_facts(self):
        nutrition_facts = {
            # 必填欄位
            'calories': Decimal(self.request.POST.get('calories')),
            'protein': Decimal(self.request.POST.get('protein')),
            'total_fat': Decimal(self.request.POST.get('total_fat')),
            'saturated_fat': Decimal(self.request.POST.get('saturated_fat')),
            'trans_fat': Decimal(self.request.POST.get('trans_fat')),
            'carbohydrate': Decimal(self.request.POST.get('carbohydrate')),
            'sugar': Decimal(self.request.POST.get('sugar')),
            'sodium': Decimal(self.request.POST.get('sodium')),
        }

        nutrition_facts = self.check_input(nutrition_facts, [
            'polyunsaturated_fat', 
            'monounsaturated_fat',

            'potassium',
            'calcium',
            'iron',
            'zinc',

            'dietary_fiber',
            'cholesterol',
            
            'vitamin_a',
            'vitamin_d',
            'vitamin_e',
            'vitamin_k',
            'vitamin_b1',
            'vitamin_b2',
            'niacin',
            'vitamin_b6',
            'vitamin_b12',
            'folate',
            'vitamin_c',
            ])

        return nutrition_facts

    def get_ingredient(self):
        switch = self.request.POST.get('is_public')
        if switch:
            is_public = True
        else:
            is_public = False
        return {
            'brand': self.request.POST.get('brand'),
            'ingredient': self.request.POST.get('ingredient'),
            'alias': self.request.POST.get('alias'),
            'quantity': Decimal(self.request.POST.get('quantity')),
            'unit': self.request.POST.get('unit'),
            'description': self.request.POST.get('description'),
            'is_public': is_public,
        }

def create_or_update_object(context: dict, Model, object=None):
    try:
        if object:      
            Model.objects.filter(pk__exact=object.pk).update(**context)
            return Model.objects.get(pk=object.pk)
        else:
            obj = Model.objects.create(**context)
            return obj
    except Exception as e:
        print("======= ERROR <Function: create_or_update_object> =======\n", e)
        
class IngredientListView(ListView):
    model = Ingredient
    template_name = 'ingredients/ingredient.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        file_template = Ingredient_File.objects.filter(is_template=True)
        ingredients = Ingredient.objects.all().order_by('-ingredient')
        
        paginator = Paginator(ingredients, self.paginate_by)

        page = self.request.GET.get('page')
        
        pages = []
        bound = 4
        previous = 0
        next = 0
        try:
            page_obj = paginator.page(page)
            if (int(page) + bound) >= paginator.num_pages:
                end = paginator.num_pages
            else:
                end = int(page) + bound
                next = end + 1
            
            if (int(page) - bound) <= 1:
                start = 1
            else:
                start = int(page) - bound
                previous = start - 1
            
        except PageNotAnInteger:
            page_obj = paginator.page(1)
            start = 1
            if (1 + bound) >= paginator.num_pages:
                end = paginator.num_pages
            else:
                end = 1 + bound
                next = end + 1
            print("=======", previous, next, "=======")
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
            if (int(paginator.num_pages) - bound) <= 1:
                start = 1
            else:
                start = int(paginator.num_pages) - bound
                previous = start - 1
            end = paginator.num_pages
            print("=======", previous, next, "=======")

        nutrition_facts = []
        for ingredient in page_obj:
            nf = ingredient.get_nutrition_facts()
            if nf:
                nutrition_facts.append(nf[0])
        
        for p in range(start, end+1):
            pages.append(p)

        context.update({
            'obj': zip(page_obj, nutrition_facts),
            'templates': file_template,
            'pages': pages,
            'previous': previous,
            'next': next,
            })
        return context

def ingredient_detail_view(request, ingredient_id):
    ingredient = Ingredient.objects.get(pk=ingredient_id)
    nutrition_facts = ingredient.get_nutrition_facts()[0]
    if ingredient != None:
        context = {
            'ingredient': ingredient,
            'nutrition_facts': nutrition_facts,
        }
        return render(request, 'ingredients/ingredient_detail.html', context)


def add_ingredient_view(request):
    if request.method == "POST":
        if request.POST.get('ingredient') \
            and request.POST.get('brand') \
            and request.POST.get('quantity') \
            and request.POST.get('unit'):

            try:
                get_input = GetInputValue(request)
                ingredient_context = get_input.get_ingredient()
                ingredient_obj = create_or_update_object(ingredient_context, Ingredient)

                nutrition_facts_context={
                    'ingredient': ingredient_obj,
                }
                nutrition_facts_context.update(get_input.get_nutrition_facts())
                nutrition_facts_obj = create_or_update_object(nutrition_facts_context, Nutrition_Facts)

            except Exception as e:
                print("========= ERROR <Function: add_ingredient_view> =========\n", e)

            return HttpResponseRedirect(reverse('ingredient'))

    return render(request, 'ingredients/ingredient_add.html')

def edit_ingredient_view(request):
    if request.method == "POST":
        ingredient = Ingredient.objects.get(pk=request.POST.get('id'))
        if ingredient != None:
            try:
                get_input = GetInputValue(request)
                ingredient_context = get_input.get_ingredient()
                create_or_update_object(ingredient_context, Ingredient, object=ingredient)

                nutrition_facts = ingredient.get_nutrition_facts()[0]
                nutrition_facts_context = get_input.get_nutrition_facts()
                create_or_update_object(nutrition_facts_context, Nutrition_Facts, object=nutrition_facts)
            except Exception as e:
                print("========= ERROR <Function: edit_ingredient_view> =========\n", e)

            return HttpResponseRedirect(reverse('ingredient'))

def delete_ingredient_view(request, ingredient_id):
    if request.method == "POST": 
        ingredient = Ingredient.objects.get(pk=ingredient_id)
        nutrition_facts = ingredient.get_nutrition_facts()[0]
        nutrition_facts.delete()
        ingredient.delete()

    return HttpResponseRedirect(reverse('ingredient'))

## 搜尋食材
def search_view(request):
    if request.method == "POST":
        search_text = request.POST['search_name']
        ingredients = Ingredient.objects.filter(Q(ingredient__contains=search_text) | Q(alias__contains=search_text))
        nutrition_facts = []
        try:
            for ingredient in ingredients:
                nf = ingredient.get_nutrition_facts()
                if nf:
                    nutrition_facts.append(nf[0])

            if ingredients:
                context={
                    'obj':  zip(ingredients, nutrition_facts),
                    'search_text': search_text,
                    'notFound': False,
                }    
            else:
                context={
                    'search_text': search_text,
                    'notFound': True,
                }   
            if 'recipe' in request.POST:
                context.update({'recipe': True})
                
            return render(request, 'ingredients/ingredient_search.html', context)
        except Exception as e:
            print("========== ERROR <Function: search_view> ==========\n", e)

    return render(request, 'ingredients/ingredient_search.html')


class IngredientFile():
    def __init__(self, file=None, dataFrame=None):
        self.file = file
        self.df = dataFrame

    ## 將上傳的檔案儲存到資料庫中
    def upload_ingredients_file(self, request):
        try:
            if request.FILES.get('file'):
                file = Ingredient_File()
                file.file = request.FILES.get('file')
                file.save()

                self.file = file
                return self.file, HTTPStatus.OK.value

            return self.file, HTTPStatus.BAD_REQUEST.value

        except Exception as e:
            print("======= ERROR <Function: upload_ingredients_file> =======\n", e)
            return file, HTTPStatus.EXPECTATION_FAILED.value

    ## 確認檔案是否符合FDA的格式，符合：回傳欄位名稱及成功(True)，不符合：回傳缺失的欄位名稱及失敗(False)
    def from_FDA_template(self, column_names):
        cols = ['是否公開(公開: V, 不公開則留白)', '樣品名稱', '俗名', '內容物描述', '食材品牌/資料來源',
            '熱量(kcal)', '粗蛋白(g)', '粗脂肪(g)', '飽和脂肪(g)', '反式脂肪(mg)', '總碳水化合物(g)', '糖質總量(g)', '鈉(mg)',
            '脂肪酸P總量(mg)', '脂肪酸M總量(mg)', '鉀(mg)', '鈣(mg)', '鐵(mg)', '鋅(mg)', '膳食纖維(g)', '膽固醇(mg)', 
            '維生素A總量(IU)', '維生素D總量(ug)', '維生素E總量(mg)', '維生素K1(ug)', '維生素K2 (MK-4)(ug)', '維生素K2 (MK-7)(ug)',
            '維生素B1(mg)', '維生素B2(mg)', '菸鹼素(mg)', '維生素B6(mg)', '維生素B12(ug)', '葉酸(ug)', '維生素C(mg)'
            ]  

        losed_cols = []
        for col in cols:
            if col not in column_names:
                losed_cols.append(col)

        if losed_cols:
            return losed_cols, False
        return cols, True
    
    ## 確認檔案是否符合我們的格式，符合：回傳欄位名稱及成功(True)，不符合：回傳缺失的欄位名稱及失敗(False)
    def from_our_template(self, column_names):
        cols = ['是否公開(公開: V, 不公開則留白)', '名稱', '俗名', '食材描述', '食材品牌/資料來源', '每一份重量', '單位(g, ml)',
            '熱量(kcal)', '蛋白質(g)', '總脂肪(g)', '飽和脂肪(g)', '反式脂肪(mg)', '總碳水化合物(g)', '糖質總量(g)', '鈉(mg)',
            '多元不飽和脂肪酸(mg)', '單元不飽和脂肪酸(mg)', '鉀(mg)', '鈣(mg)', '鐵(mg)', '鋅(mg)', '膳食纖維(g)', '膽固醇(mg)', 
            '維生素A(IU)', '維生素D(ug)', '維生素E(mg)', '維生素K(ug)',
            '維生素B1(mg)', '維生素B2(mg)', '菸鹼素(mg)', '維生素B6(mg)', '維生素B12(ug)', '葉酸(ug)', '維生素C(mg)'
            ]
        losed_cols = []
        for col in cols:
            if col not in column_names:
                losed_cols.append(col)

        if losed_cols:
            return losed_cols, False
        return cols, True

    def extract_ingredient(self, ingredient_label, r, cols, end_range=7):
        ingredient = {}
        # cols[0:5] 為 ingredient 的內容
        value = str(self.df.at[r, cols[0]])
        if value == 'V' or value == 'v':
            ingredient[ingredient_label[0]] = True

        for c in range(1, end_range):
            value = str(self.df.at[r, cols[c]])
            if value != 'nan':
                ingredient[ingredient_label[c]] = value
        
        return ingredient


    def extract_nutrition_facts(self, nutrition_facts_label, r, cols, start, start_range=5, end_range=13, set_default=False):
        nutrition_facts = {}

        for c in range(start_range, end_range):
            value = str(self.df.at[r, cols[c]])
            if value != 'nan':
                nutrition_facts[nutrition_facts_label[c-start]] = Decimal(value).quantize(Decimal('1.00'))
            elif set_default:
                nutrition_facts[nutrition_facts_label[c-start]] = Decimal('0')
            
        return nutrition_facts
    ## 依據 FDA 模板的欄位名稱來取出資料，並從到字典(ingredient, nutrition_facts)中
    def extract_from_FDA(self, ingredient_label, nutrition_facts_label, cols):
        for r in range(len(self.df)):
            # cols[0:5] 為 ingredient 的內容
            ingredient = self.extract_ingredient(ingredient_label, r, cols, end_range=5)
            # 該模板以 100g 為單位
            ingredient[ingredient_label[5]] = Decimal('100')
            ingredient[ingredient_label[6]] = 'g'

            # cols[5:34] 為 nutrition_facts 的內容
            # cols[5:13]為必填欄位
            start = 5
            nutrition_facts = self.extract_nutrition_facts(nutrition_facts_label, r, cols, start, set_default=True)
            
            # cols[13:34]為選填欄位
            nutrition_facts.update(self.extract_nutrition_facts(nutrition_facts_label, r, cols, start, start_range=13, end_range=24))
            
            # cols[24:27]為'維生素K1(ug)', '維生素K2 (MK-4)(ug)', '維生素K2 (MK-7)(ug)'
            for c in range(24, 27):
                vitamin_k_total = Decimal('0')
                value = str(self.df.at[r, cols[c]])
                if value != 'nan':
                    vitamin_k_total += Decimal(value)
            # 將'維生素K1(ug)', '維生素K2 (MK-4)(ug)', '維生素K2 (MK-7)(ug)'相加為'維生素K'
            if vitamin_k_total != Decimal('0'):
                nutrition_facts[nutrition_facts_label[19]] = vitamin_k_total.quantize(Decimal('1.00'))
            
            nutrition_facts.update(self.extract_nutrition_facts(nutrition_facts_label, r, cols, (start+2), start_range=27, end_range=34))

            print(ingredient)
            print(nutrition_facts)
            print()
            self.load_ingredients(ingredient, nutrition_facts)

    ## 依據網站提供的模板之欄位名稱來取出資料，並從到字典(ingredient, nutrition_facts)中
    def extract_from_our(self, ingredient_label, nutrition_facts_label, cols):
        for r in range(len(self.df)):

            # cols[0:7] 為 ingredient 的內容
            ingredient = self.extract_ingredient(ingredient_label, r, cols, end_range=7)
            # 將 quantity 的值轉為 decimal
            ingredient[ingredient_label[5]] = Decimal(ingredient.get(ingredient_label[5], '100'))

            # cols[7:34] 為 nutrition_facts 的內容
            # cols[7:15]為必填欄位
            start = 7 
            nutrition_facts = self.extract_nutrition_facts(nutrition_facts_label, r, cols, start, start_range=7, end_range=15, set_default=True)

            # cols[15:34]為選填欄位
            nutrition_facts.update(self.extract_nutrition_facts(nutrition_facts_label, r, cols, start, start_range=15, end_range=34))

            print(ingredient)
            print(nutrition_facts)
            print()
            self.load_ingredients(ingredient, nutrition_facts)

    ## 將資料從檔案中取出並存到資料庫中
    def extract_ingredients(self):
        ingredient_label = ['is_public', 'ingredient', 'alias', 'description', 'brand', 'quantity', 'unit']
        nutrition_facts_label = NutritionFactsInformation().get_label_list()
        
        self.df = pd.read_excel(self.file.file)
        column_names = list(self.df.columns.values)

        cols_FDA, is_FDA = self.from_FDA_template(column_names)
        if is_FDA:
            self.extract_from_FDA(ingredient_label, nutrition_facts_label, cols_FDA)
            print("====== SUCCESS <extract_from_FDA> ======")
            return True
        else:
            cols_our, is_our = self.from_our_template(column_names)
            if is_our:
                self.extract_from_our(ingredient_label, nutrition_facts_label, cols_our)
                print("====== SUCCESS <extract_from_our> ======")
                return True
            else:
                print("====== LOSE COLUMN FROM FDA ======\n", cols_FDA)
                print("====== LOSE COLUMN FROM OUR ======\n", cols_our)
                return False

    ## 新增 ingredient 及 nutrition_facts
    def load_ingredients(self, ingredient: dict, nutrition_facts: dict):
        try:
            ingredient_obj = create_or_update_object(ingredient, Ingredient)
            nutrition_facts.update({'ingredient': ingredient_obj})
            create_or_update_object(nutrition_facts, Nutrition_Facts)

        except Exception as e:
            print("========== ERROR <Function: <load_ingredients> ==========\n", e)
            

## 將要新增的食材(含營養標示)從 excel 中取出並新增到資料庫中
def extract_and_load_ingredients_view(request):
    if request.method == "POST":
        # files = Ingredient_File.objects.all()
        # file = files[2]

        # ingredient_file = IngredientFile(file=file)
        ingredient_file = IngredientFile()
        
        file, status = ingredient_file.upload_ingredients_file(request)

        if status == 200:
            print("======= url:", file.file, "=======")

            successed = ingredient_file.extract_ingredients()
            if not successed:
                print("======= 請確認檔案內容是否有缺失 =======")
        else:
            print("======= status:", status, "=======")

        return HttpResponseRedirect(reverse('ingredient'))