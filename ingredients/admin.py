from django.contrib import admin
from .models import Ingredient, Nutrition_Facts, Used_Ingredient, Ingredient_File

# Register your models here.
class NutritionFactsInline(admin.TabularInline):
    model = Nutrition_Facts

class IngredientAdmin(admin.ModelAdmin):
    inlines = [NutritionFactsInline]
    
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Nutrition_Facts)
admin.site.register(Used_Ingredient)  
admin.site.register(Ingredient_File)  
