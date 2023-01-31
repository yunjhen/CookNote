from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django import forms
# from .models import Ingredient

class IngredientForm(forms.Form):
    brand = forms.CharField(label='食材品牌', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'calories', 'placeholder': '例如: Elle&Vire 或 FDA'}))
    name = forms.CharField(label='食材名稱', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'calories', 'placeholder': '例如: 鮮奶油'}))
    quantity = forms.DecimalField(label='份量', max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'calories', 'placeholder': '必填'}))
    UNIT_CHOICES=(
        ('g', '公克/g'),
        ('ml', '毫升/ml'),
    )
    unit = forms.ChoiceField(label='單位', choices=UNIT_CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'unit'}))
   
class NutritionFactsForm(forms.Form):
    calories = forms.DecimalField(label='熱量(卡路里)', help_text='必填', max_digits=7, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'calories', 'placeholder': '必填'}))
    protein = forms.DecimalField(label='蛋白質', help_text='必填', max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'protein', 'placeholder': '必填'}))
    total_fat = forms.DecimalField(label='總脂肪', help_text='必填', max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'total_fat', 'placeholder': '必填'}))
    saturated_fat = forms.DecimalField(label='飽和脂肪', help_text='必填', max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'saturated_fat', 'placeholder': '必填'}))
    trans_fat = forms.DecimalField(label='反式脂肪', help_text='必填', max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'trans_fat', 'placeholder': '必填'}))
    polyunsaturated_fat = forms.DecimalField(label='多元不飽和脂肪', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'polyunsaturated_fat', 'placeholder': '選填'}))
    monounsaturated_fat = forms.DecimalField(label='單元不飽和脂肪', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'monounsaturated_fat', 'placeholder': '選填'}))
    carbohydrate = forms.DecimalField(label='碳水化合物', help_text='必填', max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'carbohydrate', 'placeholder': '必填'}))
    sugar = forms.DecimalField(label='糖', help_text='必填', max_digits=6, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'sugar', 'placeholder': '必填'}))
    sodium = forms.DecimalField(label='鈉', help_text='必填', max_digits=6, decimal_places=2, required=True, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'sodium', 'placeholder': '必填'}))

    potassium = forms.DecimalField(label='鉀', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'potassium', 'placeholder': '選填'}))
    calcium = forms.DecimalField(label='鈣', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'calcium', 'placeholder': '選填'}))
    iron = forms.DecimalField(label='鐵', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'iron', 'placeholder': '選填'}))
    zinc = forms.DecimalField(label='鋅', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'zinc', 'placeholder': '選填'}))

    dietary_fiber = forms.DecimalField(label='膳食纖維', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'dietary_fiber', 'placeholder': '選填'}))
    cholesterol = forms.DecimalField(label='膽固醇', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'cholesterol', 'placeholder': '選填'}))

    vitamin_a = forms.DecimalField(label='維生素A', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'vitamin_a', 'placeholder': '選填'}))
    vitamin_d = forms.DecimalField(label='維生素D', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'vitamin_d', 'placeholder': '選填'}))
    vitamin_e = forms.DecimalField(label='維生素E', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'vitamin_e', 'placeholder': '選填'}))
    vitamin_k = forms.DecimalField(label='維生素K', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'vitamin_k', 'placeholder': '選填'}))
    vitamin_b1 = forms.DecimalField(label='維生素B1', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'vitamin_b1', 'placeholder': '選填'}))
    vitamin_b2 = forms.DecimalField(label='維生素B2', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'vitamin_b2', 'placeholder': '選填'}))
    niacin = forms.DecimalField(label='菸鹼素/維他命B3', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'niacin', 'placeholder': '選填'}))
    vitamin_b6 = forms.DecimalField(label='維生素B6', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'vitamin_b6', 'placeholder': '選填'}))
    vitamin_b12 = forms.DecimalField(label='維生素B12', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'vitamin_b12', 'placeholder': '選填'}))
    folate = forms.DecimalField(label='葉酸', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'folate', 'placeholder': '選填'}))
    vitamin_c = forms.DecimalField(label='維生素C', help_text='選填', max_digits=6, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'vitamin_c', 'placeholder': '選填'}))

class UsedIngredientForm(forms.Form):
    ingredient_id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(label='食材名稱', max_length=50, widget=forms.HiddenInput())
    brand = forms.CharField(label='食材品牌', max_length=50, widget=forms.HiddenInput())
    quantity = forms.DecimalField(label='份量', max_digits=6, decimal_places=2, min_value=0.01, widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'calories', 'placeholder': '必填'}))
    UNIT_CHOICES=(
        ('g', '公克/g'),
        ('ml', '毫升/ml'),
    )
    unit = forms.ChoiceField(label='', choices=UNIT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))