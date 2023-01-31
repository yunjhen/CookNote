from django.db import models
from django.urls import reverse
from django.forms.models import model_to_dict
from django.utils import timezone

from recipes.models import Recipe
from decimal import *


class Nutrition_Facts(models.Model):
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, null=True, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    calories = models.DecimalField(max_digits=9, decimal_places=2)
    protein = models.DecimalField(max_digits=9, decimal_places=2)
    total_fat = models.DecimalField(max_digits=9, decimal_places=2)
    saturated_fat = models.DecimalField(max_digits=9, decimal_places=2)
    # 反式脂肪
    trans_fat = models.DecimalField(max_digits=9, decimal_places=2)
    # 多元不飽和脂肪
    polyunsaturated_fat = models.DecimalField(max_digits=9, decimal_places=2, default=0, null=True, blank=True)
    # 單元不飽和脂肪
    monounsaturated_fat = models.DecimalField(max_digits=9, decimal_places=2, default=0, null=True, blank=True)
    
    # 總碳水
    carbohydrate = models.DecimalField(max_digits=9, decimal_places=2)
    sugar = models.DecimalField(max_digits=9, decimal_places=2)
    sodium = models.DecimalField(max_digits=9, decimal_places=2)
    
    # 鉀
    potassium = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    # 鈣
    calcium = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    iron = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    zinc = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    # 膳食纖維
    dietary_fiber = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    # 膽固醇
    cholesterol = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    
    vitamin_a = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    vitamin_d = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    vitamin_e = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    vitamin_k = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    vitamin_b1 = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    vitamin_b2 = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    # 菸鹼素/維他命B3
    niacin = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    vitamin_b6 = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    vitamin_b12 = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    #葉酸
    folate = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    vitamin_c = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        """String for representing the Model object."""
        if self.ingredient:
            return f'<{self.pk}> (I{self.ingredient.pk} {self.ingredient.ingredient}) calories: {self.calories}/ protein: {self.protein}/ total fat: {self.total_fat}/ carbohydrate: {self.carbohydrate}'
        elif self.recipe:
            return f'<{self.pk}> (R{self.recipe.pk} {self.recipe.delicacy}) calories: {self.calories}/ protein: {self.protein}/ total fat: {self.total_fat}/ carbohydrate: {self.carbohydrate}'
        else:
            return f'<{self.pk}> calories: {self.calories}/ protein: {self.protein}/ total fat: {self.total_fat}/ carbohydrate: {self.carbohydrate}'


class Ingredient(models.Model):
    # founder = models.ForeignKey('account.Account', on_delete=models.SET_NULL, null=True)
    ingredient = models.CharField(max_length=50)
    alias = models.CharField(max_length=200, null=True, blank=True)
    brand = models.CharField(max_length=50)
    quantity = models.DecimalField(max_digits=7, decimal_places=2)
    UNIT_CHOICES=(
        ('g', 'gram'),
        ('ml', 'ml'),
    )
    unit = models.CharField(
        max_length=4,
        choices=UNIT_CHOICES,
        blank=False,
        default='g',
        )
    description = models.CharField(max_length=1000, null=True, blank=True)
    is_public = models.BooleanField(default=False)  ## False: 食材為未公開的，除了建立者以外的人無法檢視與使用


    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('ingredient-detail', args=[str(self.pk)])

    def __str__(self):
        """String for representing the Model object."""
        return f'<{self.pk}> {self.brand}, {self.ingredient} ({self.alias})'

    def get_nutrition_facts(self):
        return self.nutrition_facts_set.all()

    def get_used_ingredients(self):
        return self.used_ingredient_set.all()


class Used_Ingredient(models.Model):
    ingredient = models.ForeignKey('Ingredient', on_delete=models.RESTRICT)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, blank=True)
    serving = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        """String for representing the Model object."""
        return f'<{self.pk}> (R{self.recipe.pk} {self.recipe.delicacy}): I{self.ingredient.pk} {self.ingredient.ingredient} {self.ingredient.quantity}{self.ingredient.unit} * {self.serving}'
    
    # 食材的使用量
    def get_quantity_used(self):
        return ( self.ingredient.quantity * self.serving ).quantize(Decimal('1.00'))
 
    # 以食材的使用量計算出的熱量
    def get_calories(self):
        nutrition_facts = self.ingredient.get_nutrition_facts()[0]
        return ( nutrition_facts.calories * self.serving ).quantize(Decimal('1.00'))

    def get_nutrition_facts_dict(self):
        nutrition_facts = self.ingredient.get_nutrition_facts()
        nutrition_facts_ = model_to_dict(nutrition_facts[0])

        del nutrition_facts_['ingredient']
        del nutrition_facts_['recipe']
        del nutrition_facts_['id']
        
        for key, value in nutrition_facts_.items():
            nutrition_facts_[key] = value * self.serving

        return nutrition_facts_


class Ingredient_File(models.Model):
    file = models.FileField(upload_to='ingredients/files', null=True, blank=True)
    upload_date = models.DateField(default=timezone.now)
    is_template = models.BooleanField(default=False)

    def __str__(self):
        return f'<{self.pk}> {self.file} upload_date: {self.upload_date}'
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)