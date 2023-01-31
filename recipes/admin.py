from django.contrib import admin
from .models import Recipe, Recipe_Photo, Step, Step_Photo
from ingredients.models import Used_Ingredient

# Register your models here.
class UsedIngredientInline(admin.TabularInline):
    model = Used_Ingredient

class StepInline(admin.TabularInline):
    model = Step

class RecipeAdmin(admin.ModelAdmin):
    inlines = [UsedIngredientInline, StepInline]
    
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Recipe_Photo) 
admin.site.register(Step) 
admin.site.register(Step_Photo) 